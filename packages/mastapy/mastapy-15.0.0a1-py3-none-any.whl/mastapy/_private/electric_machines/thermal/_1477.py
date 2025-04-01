"""ThermalRotor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_THERMAL_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalRotor"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1422
    from mastapy._private.electric_machines.thermal import _1454, _1464
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _202,
        _217,
    )

    Self = TypeVar("Self", bound="ThermalRotor")
    CastSelf = TypeVar("CastSelf", bound="ThermalRotor._Cast_ThermalRotor")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalRotor:
    """Special nested class for casting ThermalRotor to subclasses."""

    __parent__: "ThermalRotor"

    @property
    def thermal_rotor(self: "CastSelf") -> "ThermalRotor":
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
class ThermalRotor(_0.APIBase):
    """ThermalRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def front_bearing_radial_thermal_resistance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "FrontBearingRadialThermalResistance"
        )

        if temp is None:
            return 0.0

        return temp

    @front_bearing_radial_thermal_resistance.setter
    @enforce_parameter_types
    def front_bearing_radial_thermal_resistance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FrontBearingRadialThermalResistance",
            float(value) if value is not None else 0.0,
        )

    @property
    def has_shaft_cooling_channel(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasShaftCoolingChannel")

        if temp is None:
            return False

        return temp

    @has_shaft_cooling_channel.setter
    @enforce_parameter_types
    def has_shaft_cooling_channel(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasShaftCoolingChannel",
            bool(value) if value is not None else False,
        )

    @property
    def has_single_shaft_cooling_outlet(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasSingleShaftCoolingOutlet")

        if temp is None:
            return False

        return temp

    @has_single_shaft_cooling_outlet.setter
    @enforce_parameter_types
    def has_single_shaft_cooling_outlet(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasSingleShaftCoolingOutlet",
            bool(value) if value is not None else False,
        )

    @property
    def inlet_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InletPosition")

        if temp is None:
            return 0.0

        return temp

    @inlet_position.setter
    @enforce_parameter_types
    def inlet_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InletPosition", float(value) if value is not None else 0.0
        )

    @property
    def interlaminate_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InterlaminateMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @interlaminate_material.setter
    @enforce_parameter_types
    def interlaminate_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InterlaminateMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def rear_bearing_radial_thermal_resistance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RearBearingRadialThermalResistance"
        )

        if temp is None:
            return 0.0

        return temp

    @rear_bearing_radial_thermal_resistance.setter
    @enforce_parameter_types
    def rear_bearing_radial_thermal_resistance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RearBearingRadialThermalResistance",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaft_bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftBore")

        if temp is None:
            return 0.0

        return temp

    @shaft_bore.setter
    @enforce_parameter_types
    def shaft_bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftBore", float(value) if value is not None else 0.0
        )

    @property
    def shaft_coolant_fluid(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ShaftCoolantFluid", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @shaft_coolant_fluid.setter
    @enforce_parameter_types
    def shaft_coolant_fluid(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ShaftCoolantFluid",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def shaft_cooling_inlet_location(self: "Self") -> "_1464.InletLocation":
        """mastapy.electric_machines.thermal.InletLocation"""
        temp = pythonnet_property_get(self.wrapped, "ShaftCoolingInletLocation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.Thermal.InletLocation"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1464", "InletLocation"
        )(value)

    @shaft_cooling_inlet_location.setter
    @enforce_parameter_types
    def shaft_cooling_inlet_location(
        self: "Self", value: "_1464.InletLocation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.InletLocation"
        )
        pythonnet_property_set(self.wrapped, "ShaftCoolingInletLocation", value)

    @property
    def shaft_front_extension_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftFrontExtensionLength")

        if temp is None:
            return 0.0

        return temp

    @shaft_front_extension_length.setter
    @enforce_parameter_types
    def shaft_front_extension_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftFrontExtensionLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaft_front_extension_outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftFrontExtensionOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_front_extension_outer_diameter.setter
    @enforce_parameter_types
    def shaft_front_extension_outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftFrontExtensionOuterDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaft_rear_extension_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftRearExtensionLength")

        if temp is None:
            return 0.0

        return temp

    @shaft_rear_extension_length.setter
    @enforce_parameter_types
    def shaft_rear_extension_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftRearExtensionLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def shaft_rear_extension_outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftRearExtensionOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_rear_extension_outer_diameter.setter
    @enforce_parameter_types
    def shaft_rear_extension_outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftRearExtensionOuterDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    def specify_heat_transfer_coefficient_for_rotor_outer_boundary(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyHeatTransferCoefficientForRotorOuterBoundary"
        )

        if temp is None:
            return False

        return temp

    @specify_heat_transfer_coefficient_for_rotor_outer_boundary.setter
    @enforce_parameter_types
    def specify_heat_transfer_coefficient_for_rotor_outer_boundary(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyHeatTransferCoefficientForRotorOuterBoundary",
            bool(value) if value is not None else False,
        )

    @property
    def heat_transfer_coefficient_specification_for_shaft_cooling(
        self: "Self",
    ) -> "_217.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientSpecificationForShaftCooling"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor(self: "Self") -> "_1422.Rotor":
        """mastapy.electric_machines.Rotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor_outer_boundary_htc(
        self: "Self",
    ) -> "_217.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorOuterBoundaryHTC")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor_to_magnet_interface_gap(self: "Self") -> "_202.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorToMagnetInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor_to_shaft_interface_gap(self: "Self") -> "_202.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorToShaftInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_channel(self: "Self") -> "_1454.Channel":
        """mastapy.electric_machines.thermal.Channel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftChannel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalRotor":
        """Cast to another type.

        Returns:
            _Cast_ThermalRotor
        """
        return _Cast_ThermalRotor(self)
