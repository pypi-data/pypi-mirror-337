"""ThermalElectricMachine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1379

_THERMAL_ELECTRIC_MACHINE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalElectricMachine"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1380, _1421
    from mastapy._private.electric_machines.thermal import (
        _1457,
        _1466,
        _1470,
        _1472,
        _1474,
        _1477,
        _1478,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses import _1495
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _187

    Self = TypeVar("Self", bound="ThermalElectricMachine")
    CastSelf = TypeVar(
        "CastSelf", bound="ThermalElectricMachine._Cast_ThermalElectricMachine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalElectricMachine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalElectricMachine:
    """Special nested class for casting ThermalElectricMachine to subclasses."""

    __parent__: "ThermalElectricMachine"

    @property
    def electric_machine_design_base(
        self: "CastSelf",
    ) -> "_1379.ElectricMachineDesignBase":
        return self.__parent__._cast(_1379.ElectricMachineDesignBase)

    @property
    def thermal_electric_machine(self: "CastSelf") -> "ThermalElectricMachine":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class ThermalElectricMachine(_1379.ElectricMachineDesignBase):
    """ThermalElectricMachine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ELECTRIC_MACHINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def include_result_locations_from_electric_machine_design(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeResultLocationsFromElectricMachineDesign"
        )

        if temp is None:
            return False

        return temp

    @include_result_locations_from_electric_machine_design.setter
    @enforce_parameter_types
    def include_result_locations_from_electric_machine_design(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeResultLocationsFromElectricMachineDesign",
            bool(value) if value is not None else False,
        )

    @property
    def machine_orientation(self: "Self") -> "_187.CylinderOrientation":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.CylinderOrientation"""
        temp = pythonnet_property_get(self.wrapped, "MachineOrientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis.CylinderOrientation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis._187",
            "CylinderOrientation",
        )(value)

    @machine_orientation.setter
    @enforce_parameter_types
    def machine_orientation(self: "Self", value: "_187.CylinderOrientation") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis.CylinderOrientation",
        )
        pythonnet_property_set(self.wrapped, "MachineOrientation", value)

    @property
    def electric_machine(self: "Self") -> "_1380.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachine")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def front_thermal_end_winding(self: "Self") -> "_1474.ThermalEndWinding":
        """mastapy.electric_machines.thermal.ThermalEndWinding

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontThermalEndWinding")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rear_thermal_end_winding(self: "Self") -> "_1474.ThermalEndWinding":
        """mastapy.electric_machines.thermal.ThermalEndWinding

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RearThermalEndWinding")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_locations_specification(
        self: "Self",
    ) -> "_1421.ResultsLocationsSpecification":
        """mastapy.electric_machines.ResultsLocationsSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsLocationsSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor(self: "Self") -> "_1477.ThermalRotor":
        """mastapy.electric_machines.thermal.ThermalRotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor_setup(self: "Self") -> "_1466.RotorSetup":
        """mastapy.electric_machines.thermal.RotorSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def selected_setup(self: "Self") -> "_1472.ThermalElectricMachineSetup":
        """mastapy.electric_machines.thermal.ThermalElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator(self: "Self") -> "_1478.ThermalStator":
        """mastapy.electric_machines.thermal.ThermalStator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator_setup(self: "Self") -> "_1470.StatorSetup":
        """mastapy.electric_machines.thermal.StatorSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cutouts_for_thermal_analysis(
        self: "Self",
    ) -> "List[_1457.CutoutsForThermalAnalysis]":
        """List[mastapy.electric_machines.thermal.CutoutsForThermalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutoutsForThermalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def load_case_groups(self: "Self") -> "List[_1495.ThermalLoadCaseGroup]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCaseGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def setups(self: "Self") -> "List[_1472.ThermalElectricMachineSetup]":
        """List[mastapy.electric_machines.thermal.ThermalElectricMachineSetup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def add_load_case_group(
        self: "Self", name: "str" = "Load Case Group"
    ) -> "_1495.ThermalLoadCaseGroup":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCaseGroup

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddLoadCaseGroup", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def add_setup(self: "Self") -> "_1472.ThermalElectricMachineSetup":
        """mastapy.electric_machines.thermal.ThermalElectricMachineSetup"""
        method_result = pythonnet_method_call(self.wrapped, "AddSetup")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def duplicate_setup(
        self: "Self", setup: "_1472.ThermalElectricMachineSetup"
    ) -> "_1472.ThermalElectricMachineSetup":
        """mastapy.electric_machines.thermal.ThermalElectricMachineSetup

        Args:
            setup (mastapy.electric_machines.thermal.ThermalElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "DuplicateSetup", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def remove_all_load_case_groups(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllLoadCaseGroups")

    @enforce_parameter_types
    def remove_load_case_group_named(self: "Self", name: "str") -> "bool":
        """bool

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "RemoveLoadCaseGroupNamed", name if name else ""
        )
        return method_result

    @enforce_parameter_types
    def setup_named(self: "Self", name: "str") -> "_1472.ThermalElectricMachineSetup":
        """mastapy.electric_machines.thermal.ThermalElectricMachineSetup

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "SetupNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_remove_load_case_group(
        self: "Self", load_case_group: "_1495.ThermalLoadCaseGroup"
    ) -> "bool":
        """bool

        Args:
            load_case_group (mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCaseGroup)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryRemoveLoadCaseGroup",
            load_case_group.wrapped if load_case_group else None,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalElectricMachine":
        """Cast to another type.

        Returns:
            _Cast_ThermalElectricMachine
        """
        return _Cast_ThermalElectricMachine(self)
