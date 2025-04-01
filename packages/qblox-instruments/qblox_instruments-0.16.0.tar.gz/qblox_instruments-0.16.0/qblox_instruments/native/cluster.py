# ----------------------------------------------------------------------------
# Description    : Cluster native interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import warnings
from collections.abc import Iterable, Iterator
from functools import partial
from typing import Any, Optional, Union

import qblox_instruments.native.generic_func as gf
from qblox_instruments import DeviceInfo, InstrumentClass, InstrumentType, TypeHandle, resolve
from qblox_instruments.docstring_helpers import copy_docstr, partial_with_numpy_doc
from qblox_instruments.ieee488_2 import (
    ClusterDummyTransport,
    DummyBinnedAcquisitionData,
    DummyScopeAcquisitionData,
    IpTransport,
)
from qblox_instruments.scpi import Cluster as ClusterScpi

SLOT_DESCRIPTION = "The slot index of the module being referred to."
SLOT_PARAM_DICT_INT = {"slot": ("int", SLOT_DESCRIPTION)}
SLOT_PARAM_DICT_OPT = {"slot": ("Optional[int]", SLOT_DESCRIPTION)}

# -- class -------------------------------------------------------------------


class Cluster(ClusterScpi):
    """
    Class that provides the native API for the Cluster. It provides methods
    to control all functions and features provided by the Cluster.

    Note that the bulk of the functionality of this class is contained in the
    :mod:`~qblox_instruments.native.generic_func` module so that this
    functionality can be shared between instruments.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        identifier: str,
        port: Optional[int] = None,
        debug: Optional[int] = None,
        dummy_cfg: Optional[dict] = None,
    ) -> None:
        """
        Creates Cluster native interface object.

        Parameters
        ----------
        identifier : str
            Instrument identifier. See :func:`~qblox_instruments.resolve()`
            for more information.
        port : Optional[int]
            Instrument port. If None, this will be determined automatically.
        debug : Optional[int]
            Debug level (0 | None = normal, 1 = no version check, >1 = no
            version or error checking).
        dummy_cfg : Optional[dict]
            Configure as dummy using this configuration. For each slot that
            needs to be occupied by a module add the slot index as key and
            specify the type of module in the slot using the type
            :class:`~qblox_instruments.ClusterType`.

        Raises
        ----------
        RuntimeError
            Instrument cannot be reached due to invalid IP configuration.
        ConnectionError
            Instrument type is not supported.
        """

        # Create transport layer (dummy or socket interface)
        self._dummy_config_present = False
        if dummy_cfg is not None:
            self._dummy_config_present = True
            self._transport = ClusterDummyTransport(dummy_cfg)
            if debug is None:
                debug = 1
        else:
            addr_info = resolve(identifier)
            if addr_info.protocol != "ip":
                raise RuntimeError(
                    f"Instrument cannot be reached due to invalid IP configuration. "
                    f"Use qblox-pnp tool to rectify; serial number is {addr_info.address}"
                )
            host = addr_info.address
            if port is None:
                port = addr_info.scpi_port
            self._transport = IpTransport(host=host, port=port)
            if debug is None:
                debug = 0

        # Initialize parent class.
        super().__init__(self._transport, debug)

        # Set instrument type handle
        self._cmm_dev_info = DeviceInfo.from_idn(super()._get_idn())
        model = self._cmm_dev_info.model
        self._type_handle = TypeHandle(model)
        if not self._type_handle.is_mm_type:
            raise ConnectionError(f"Unsupported instrument type detected ({self.instrument_type})")

        # Get a dictionary of SCPI and native functions that the functions in
        # the generic_func module require to operate. Create a function
        # reference container that we use to pass references to those functions
        # to functions in the generic_func module.
        self._funcs = gf.FuncRefs(self)
        for attr_name in self._funcs.funcs:
            if self._funcs.funcs[attr_name] is None and hasattr(super(), attr_name):
                self._funcs.register(getattr(super(), attr_name))

        self.__debug = debug
        self._create_mod_handles()

    @property
    def is_dummy(self) -> bool:
        return self._dummy_config_present

    def _create_mod_handles(self, slot: Optional[int] = None) -> None:
        """
        Set up module-specific type and function reference handles for each
        module slot or a specific slot if provided. This method initializes and
        populates the `_mod_handles` dictionary with information about the modules.
        It retrieves module information, checks for firmware version mismatches,
        and sets up type handles and function references for the modules.

        Parameters
        ----------
        slot : Optional[int]
            The slot to update. If None, updates all slots.

        Raises
        ----------
        ConnectionError
            If there is a mismatch between the application version of the CMM
            and a module, and debug mode is not enabled. This requires a
            firmware update for the entire cluster.
        """

        # Set module specific type and FuncRefs handles
        if slot is None:
            # No specific slot provided, update all slots
            self._mod_handles = {}
            slot_info = self.get_json_description().get("modules", {})
        else:
            # Only update the specified slot
            self._mod_handles.pop(slot, None)
            slot_info = (
                {slot: self.get_json_description()["modules"][str(slot)]}
                if str(slot) in self.get_json_description().get("modules", {})
                else {}
            )

        for slot_str, info in slot_info.items():
            slot_id = int(slot_str)
            mod_dev_info = DeviceInfo.from_dict(info)

            # Module type handle
            model = mod_dev_info.model
            mod_type_handle = TypeHandle(model)
            if "is_rf" not in info:
                warnings.warn(
                    f"Module in slot {slot_id} has responded with incomplete information "
                    f"(missing `is_rf` field) due to an incompatible firmware version. "
                    f"Please proceed with caution."
                )
            mod_type_handle._is_rf_type = bool(info.get("is_rf", False))
            mod_type_handle._is_eom_type = bool(info.get("qtm_eom", False))

            # Module FuncRefs
            mod_funcs = self._create_module_funcrefs(slot_id)

            # Update module handles dictionary
            self._mod_handles[slot_id] = {
                "serial": mod_dev_info.serial,
                "type_handle": mod_type_handle,
                "func_refs": mod_funcs,
            }

    # ------------------------------------------------------------------------
    def _create_module_funcrefs(self, slot: int) -> gf.FuncRefs:
        """
        Create function reference container object for a specific slot. This
        means that SCPI and native layer methods are customized using
        functools.partial to operate on a specific slot. The resulting methods
        are added to the function reference container, so that they can be used
        by the generic_func module.

        Parameters
        ----------
        slot : int
            Slot index to create function reference container for.

        Returns
        ----------
        FuncRefs
            Function reference container specific to single slot.
        """

        # Non-slot specific attributes
        funcs = gf.FuncRefs(self)
        funcs.register(getattr(super(), "_write"))
        funcs.register(getattr(super(), "_read_bin"))
        funcs.register(getattr(super(), "_flush_line_end"))

        # Slot specific attributes
        rb = super()._read_bin
        part_cmd = f"SLOT{slot}:SEQuencer"
        awg_wlist_rb = gf.create_read_bin(rb, part_cmd + "{}:AWG:WLISt?")
        acq_wlist_rb = gf.create_read_bin(rb, part_cmd + "{}:ACQ:WLISt?")
        acq_data_rb = gf.create_read_bin(rb, part_cmd + '{}:ACQ:ALISt:ACQuisition:DATA? "{}"')
        acq_list_rb = gf.create_read_bin(rb, part_cmd + "{}:ACQ:ALISt?")

        funcs.register(awg_wlist_rb, "_get_awg_waveforms")
        funcs.register(acq_wlist_rb, "_get_acq_weights")
        funcs.register(acq_data_rb, "_get_acq_acquisition_data")
        funcs.register(acq_list_rb, "_get_acq_acquisitions")

        funcs.register(partial_with_numpy_doc(self._is_qcm_type, slot), "is_qcm_type")
        funcs.register(partial_with_numpy_doc(self._is_qrm_type, slot), "is_qrm_type")
        funcs.register(partial_with_numpy_doc(self._is_qtm_type, slot), "is_qtm_type")
        funcs.register(partial_with_numpy_doc(self._is_qdm_type, slot), "is_qdm_type")
        funcs.register(partial_with_numpy_doc(self._is_linq_type, slot), "is_linq_type")
        funcs.register(partial_with_numpy_doc(self._is_qrc_type, slot), "is_qrc_type")
        funcs.register(partial_with_numpy_doc(self._is_rf_type, slot), "is_rf_type")
        funcs.register(partial_with_numpy_doc(self._is_eom_type, slot), "is_eom_type")

        # Remaining slot specific attributes
        for attr_name in funcs.funcs:
            if funcs.funcs[attr_name] is None and hasattr(super(), attr_name):
                attr = partial(getattr(super(), attr_name), slot)
                funcs.register(attr, attr_name)

        return funcs

    # ------------------------------------------------------------------------
    @property
    def instrument_class(self) -> InstrumentClass:
        """
        Get instrument class (e.g. Cluster).

        Returns
        ----------
        InstrumentClass
            Instrument class
        """

        return self._type_handle.instrument_class

    # ------------------------------------------------------------------------
    @property
    def instrument_type(self) -> InstrumentType:
        """
        Get instrument type (e.g. MM, QRM, QCM).

        Returns
        ----------
        InstrumentType
            Instrument type
        """

        return self._type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _present_at_init(self, slot: int) -> tuple:
        """
        Get an indication of module presence during initialization of this
        object for a specific slot in the Cluster and return the associated
        module type handle and function reference container if present.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        TypeHandle
            Module type handle
        FuncRefs
            Function reference container

        Raises
        ----------
        KeyError
            Module is not available.
        """

        if slot in self._mod_handles:
            return (
                self._mod_handles[slot]["type_handle"],
                self._mod_handles[slot]["func_refs"],
            )
        else:
            raise KeyError(f"Module at slot {slot} is not available.")

    # ------------------------------------------------------------------------
    def _module_type(self, slot: int) -> InstrumentType:
        """
        Get indexed module's type (e.g. QRM, QCM, QTM, QDM, LINQ, QRC).

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        InstrumentType
            Module type
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _is_qcm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QCM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            True if module is of type QCM.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qcm_type

    # ------------------------------------------------------------------------
    def _is_qrm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QRM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QRM.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qrm_type

    # ------------------------------------------------------------------------
    def _is_qtm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QTM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QTM.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qtm_type

    # ------------------------------------------------------------------------
    def _is_qdm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QDM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QDM.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qdm_type

    # ------------------------------------------------------------------------
    def _is_eom_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type EOM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type EOM.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_eom_type

    # ------------------------------------------------------------------------
    def _is_linq_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type LINQ

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type LINQ.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_linq_type

    # ------------------------------------------------------------------------
    def _is_qrc_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QRC.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QRC.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qrc_type

    # ------------------------------------------------------------------------
    def _is_rf_type(self, slot: int) -> bool:
        """
        Return if indexed module has RF functionality.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module has RF functionality.
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_rf_type

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_scpi_commands)
    def _get_scpi_commands(self) -> dict:
        return gf.get_scpi_commands(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_idn)
    def get_idn(self) -> dict:
        return gf.get_idn(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_system_status)
    def get_system_status(self) -> gf.SystemStatus:
        return gf.get_system_status(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_acq_scope_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_acq_scope_config(self, slot: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_acq_scope_config(funcs, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_scope_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_scope_config(self, slot: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_scope_config(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_acq_scope_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_acq_scope_config_val(self, slot: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_acq_scope_config_val(funcs, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_scope_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_scope_config_val(self, slot: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_scope_config_val(funcs, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_channel_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_channel_config(self, slot: int, channel: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_channel_config(funcs, channel, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_output_normalized_amplitude, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_output_normalized_amplitude(self, slot: int, channel: int, amplitude: float) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_output_normalized_amplitude(funcs, channel, amplitude)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_output_normalized_amplitude, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_output_normalized_amplitude(self, slot: int, channel: int) -> float:
        _, funcs = self._present_at_init(slot)
        return gf.get_output_normalized_amplitude(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_pulse_output_offset, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_pulse_output_offset(self, slot: int, channel: int, offset: float) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_pulse_output_offset(funcs, channel, offset)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_pulse_output_offset, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_pulse_output_offset(self, slot: int, channel: int) -> float:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_pulse_output_offset(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_pulse_width_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_pulse_width_config(self, slot: int, channel: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_pulse_width_config(funcs, channel, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_pulse_width_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_pulse_width_config(self, slot: int, channel: int) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_pulse_width_config(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_config(self, slot: int, channel: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_config(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_status, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_status(self, slot: int, channel: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_status(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_channel_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_channel_config_val(self, slot: int, channel: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_channel_config_val(funcs, channel, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_config_val(self, slot: int, channel: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_config_val(funcs, channel, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_status_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_status_val(self, slot: int, channel: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_status_val(funcs, channel, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_quad_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_quad_config(self, slot: int, quad: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_quad_config(funcs, quad, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_quad_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_quad_config(self, slot: int, quad: int) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_quad_config(funcs, quad)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_quad_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_quad_config_val(self, slot: int, quad: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_quad_config_val(funcs, quad, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_quad_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_quad_config_val(self, slot: int, quad: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_quad_config_val(funcs, quad, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_program, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_program(self, slot: int, sequencer: int, program: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_program(funcs, sequencer, program)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_config(self, slot: int, sequencer: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config(funcs, sequencer, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_config(self, slot: int, sequencer: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_config_val(self, slot: int, sequencer: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config_val(funcs, sequencer, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_config_val(self, slot: int, sequencer: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config_val(funcs, sequencer, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(
        gf.set_sequencer_config_rotation_matrix,
        params_to_add=SLOT_PARAM_DICT_INT,
    )
    def _set_sequencer_config_rotation_matrix(
        self, slot: int, sequencer: int, phase_incr: float
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config_rotation_matrix(funcs, sequencer, phase_incr)

    # ------------------------------------------------------------------------
    @copy_docstr(
        gf.get_sequencer_config_rotation_matrix,
        params_to_add=SLOT_PARAM_DICT_INT,
    )
    def _get_sequencer_config_rotation_matrix(self, slot: int, sequencer: int) -> float:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config_rotation_matrix(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_connect_out, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_connect_out(
        self, slot: int, sequencer: int, output: int, state: str
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_connect_out(funcs, sequencer, output, state)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_connect_out, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_connect_out(self, slot: int, sequencer: int, output: int) -> str:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_connect_out(funcs, sequencer, output)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_connect_acq, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_connect_acq(self, slot: int, sequencer: int, path: int, state: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_connect_acq(funcs, sequencer, path, state)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_connect_acq, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_connect_acq(self, slot: int, sequencer: int, path: int) -> str:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_connect_acq(funcs, sequencer, path)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_output_latency, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_output_latency(self, slot: int, output: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_output_latency(funcs, output)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_pre_distortion_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_pre_distortion_config(self, slot: int, config: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_pre_distortion_config(funcs, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_pre_distortion_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_pre_distortion_config(self, slot: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_pre_distortion_config(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_pre_distortion_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_pre_distortion_config_val(self, slot: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_pre_distortion_config_val(funcs, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_pre_distortion_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_pre_distortion_config_val(self, slot: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_pre_distortion_config_val(funcs, keys)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.disconnect_outputs, params_to_add=SLOT_PARAM_DICT_INT)
    def _disconnect_outputs(self, slot: int) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.disconnect_outputs(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.disconnect_inputs, params_to_add=SLOT_PARAM_DICT_INT)
    def _disconnect_inputs(self, slot: int) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.disconnect_inputs(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.iter_connections, params_to_add=SLOT_PARAM_DICT_INT)
    def _iter_connections(self, slot: int) -> Iterator[tuple[int, str, str]]:
        _, funcs = self._present_at_init(slot)
        return gf.iter_connections(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.sequencer_connect, params_to_add=SLOT_PARAM_DICT_INT)
    def _sequencer_connect(self, slot: int, sequencer: int, *connections: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.sequencer_connect(funcs, sequencer, *connections)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.arm_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def arm_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Arm sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Arm all sequencers within a module

        return gf.arm_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.start_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def start_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Start sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Start all sequencers within a module

        return gf.start_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.stop_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def stop_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Stop sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Stop all sequencers within a module

        return gf.stop_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.clear_sequencer_flags, params_to_add=SLOT_PARAM_DICT_OPT)
    def clear_sequencer_flags(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Clear sequencer flags across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Clear all sequencers flags within a module

        return gf.clear_sequencer_flags(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_status, params_to_add=SLOT_PARAM_DICT_INT)
    def get_sequencer_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> gf.SequencerStatus:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_status(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.arm_scope_trigger, params_to_add=SLOT_PARAM_DICT_OPT)
    def arm_scope_trigger(self, slot: Optional[int] = None) -> None:
        if slot is not None:
            _, funcs = self._present_at_init(slot)
        else:
            slot = ""  # Arm scope triggers across all modules
            funcs = self._funcs

        return gf.arm_scope_trigger(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_waveforms, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_waveforms(self, slot: int, sequencer: int, waveforms: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_waveforms(funcs, sequencer, waveforms)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_waveform, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_waveform(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_waveform(funcs, sequencer, name, all)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_waveforms, params_to_add=SLOT_PARAM_DICT_INT)
    def get_waveforms(self, slot: int, sequencer: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_waveforms(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_weights, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_weights(self, slot: int, sequencer: int, weights: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_weights(funcs, sequencer, weights)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_weight, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_weight(self, slot: int, sequencer: int, name: str = "", all: bool = False) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_weight(funcs, sequencer, name, all)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_weights, params_to_add=SLOT_PARAM_DICT_INT)
    def get_weights(self, slot: int, sequencer: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_weights(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acquisition_status, params_to_add=SLOT_PARAM_DICT_INT)
    def get_acquisition_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> bool:
        _, funcs = self._present_at_init(slot)
        return gf.get_acquisition_status(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_acquisitions, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_acquisitions(self, slot: int, sequencer: int, acquisitions: dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_acquisitions(funcs, sequencer, acquisitions)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_acquisition, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_acquisition(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_acquisition(funcs, sequencer, name, all)

    # --------------------------------------------------------------------------
    @copy_docstr(gf.delete_acquisition_data, params_to_add=SLOT_PARAM_DICT_INT)
    def delete_acquisition_data(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_acquisition_data(funcs, sequencer, name, all)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.store_scope_acquisition, params_to_add=SLOT_PARAM_DICT_INT)
    def store_scope_acquisition(self, slot: int, sequencer: int, name: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.store_scope_acquisition(funcs, sequencer, name)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_acquisition_data, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_acquisition_data(self, slot: int, sequencer: int, name: str) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_acquisition_data(self, funcs, sequencer, name)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acquisitions, params_to_add=SLOT_PARAM_DICT_INT)
    def get_acquisitions(self, slot: int, sequencer: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acquisitions(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.scope_trigger_arm, params_to_add=SLOT_PARAM_DICT_INT)
    def scope_trigger_arm(self, slot: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.scope_trigger_arm(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_scope_data, params_to_add=SLOT_PARAM_DICT_INT)
    def get_scope_data(self, slot: int, io_channel: int) -> dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_scope_data(funcs, io_channel)

    # --------------------------------------------------------------------------
    def delete_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Optional[int] = None,
        acq_index_name: Optional[str] = None,
    ) -> None:
        """
        Delete all dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Optional[int]
            Sequencer.
        acq_index_name : Optional[str]
            Acquisition index name.
        """

        self._transport.delete_dummy_binned_acquisition_data(slot_idx, sequencer, acq_index_name)

    # --------------------------------------------------------------------------
    def set_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: int,
        acq_index_name: str,
        data: Iterable[Union[DummyBinnedAcquisitionData, None]],
    ) -> None:
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : int
            Sequencer.
        acq_index_name : str
            Acquisition index name.
        data : Iterable[Union[DummyBinnedAcquisitionData, None]]
            Dummy data for the binned acquisition.
            An iterable of all the bin values.
        """

        self._transport.set_dummy_binned_acquisition_data(slot_idx, sequencer, acq_index_name, data)

    # --------------------------------------------------------------------------
    def delete_dummy_scope_acquisition_data(
        self, slot_idx: int, sequencer: Union[int, None]
    ) -> None:
        """
        Delete dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.
        """

        self._transport.delete_dummy_scope_acquisition_data(slot_idx)

    # --------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Union[int, None],
        data: DummyScopeAcquisitionData,
    ) -> None:
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.
        """

        self._transport.set_dummy_scope_acquisition_data(slot_idx, data)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequence, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequence(
        self,
        slot: int,
        sequencer: int,
        sequence: Union[str, dict[str, Any]],
        validation_enable: bool = True,
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequence(funcs, sequencer, sequence, validation_enable)

    # ------------------------------------------------------------------------
    def _get_modules_present(self, slot: int) -> bool:
        """
        Get an indication of module presence for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            Module presence.
        """

        return (int(super()._get_modules_present()) >> (slot - 1)) & 1 == 1

    def _get_modules_connected(self, slot: int) -> bool:
        """
        Get an indication of module connection for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            Module connection
        """
        keys = super()._get_mods_info().keys()
        return slot in [int(key.split()[-1]) for key in keys]
