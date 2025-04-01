"""ThermalHousing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
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
_THERMAL_HOUSING = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalHousing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines.thermal import _1454, _1456, _1462, _1473
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _202

    Self = TypeVar("Self", bound="ThermalHousing")
    CastSelf = TypeVar("CastSelf", bound="ThermalHousing._Cast_ThermalHousing")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalHousing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalHousing:
    """Special nested class for casting ThermalHousing to subclasses."""

    __parent__: "ThermalHousing"

    @property
    def thermal_housing(self: "CastSelf") -> "ThermalHousing":
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
class ThermalHousing(_0.APIBase):
    """ThermalHousing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_HOUSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_distance_between_channels(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialDistanceBetweenChannels")

        if temp is None:
            return 0.0

        return temp

    @axial_distance_between_channels.setter
    @enforce_parameter_types
    def axial_distance_between_channels(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialDistanceBetweenChannels",
            float(value) if value is not None else 0.0,
        )

    @property
    def channel_average_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelAverageHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    def channel_average_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelAverageWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def channel_cutout_average_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelCutoutAverageHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    def channel_cutout_average_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelCutoutAverageWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def circumferential_distance_between_channels(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CircumferentialDistanceBetweenChannels"
        )

        if temp is None:
            return 0.0

        return temp

    @circumferential_distance_between_channels.setter
    @enforce_parameter_types
    def circumferential_distance_between_channels(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CircumferentialDistanceBetweenChannels",
            float(value) if value is not None else 0.0,
        )

    @property
    def coolant_fluid(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "CoolantFluid", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @coolant_fluid.setter
    @enforce_parameter_types
    def coolant_fluid(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "CoolantFluid",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def cooling_jacket_axial_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoolingJacketAxialLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cooling_jacket_axial_length.setter
    @enforce_parameter_types
    def cooling_jacket_axial_length(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoolingJacketAxialLength", value)

    @property
    def cooling_jacket_type(self: "Self") -> "_1456.CoolingJacketType":
        """mastapy.electric_machines.thermal.CoolingJacketType"""
        temp = pythonnet_property_get(self.wrapped, "CoolingJacketType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.Thermal.CoolingJacketType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1456", "CoolingJacketType"
        )(value)

    @cooling_jacket_type.setter
    @enforce_parameter_types
    def cooling_jacket_type(self: "Self", value: "_1456.CoolingJacketType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.CoolingJacketType"
        )
        pythonnet_property_set(self.wrapped, "CoolingJacketType", value)

    @property
    def critical_reynolds_number(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CriticalReynoldsNumber")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @critical_reynolds_number.setter
    @enforce_parameter_types
    def critical_reynolds_number(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CriticalReynoldsNumber", value)

    @property
    def flow_direction(self: "Self") -> "_1462.HousingFlowDirection":
        """mastapy.electric_machines.thermal.HousingFlowDirection"""
        temp = pythonnet_property_get(self.wrapped, "FlowDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.Thermal.HousingFlowDirection"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1462", "HousingFlowDirection"
        )(value)

    @flow_direction.setter
    @enforce_parameter_types
    def flow_direction(self: "Self", value: "_1462.HousingFlowDirection") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.HousingFlowDirection"
        )
        pythonnet_property_set(self.wrapped, "FlowDirection", value)

    @property
    def housing_active_axial_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HousingActiveAxialLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def housing_front_overhang_axial_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HousingFrontOverhangAxialLength")

        if temp is None:
            return 0.0

        return temp

    @housing_front_overhang_axial_length.setter
    @enforce_parameter_types
    def housing_front_overhang_axial_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HousingFrontOverhangAxialLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def housing_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "HousingMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @housing_material.setter
    @enforce_parameter_types
    def housing_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "HousingMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def housing_rear_overhang_axial_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HousingRearOverhangAxialLength")

        if temp is None:
            return 0.0

        return temp

    @housing_rear_overhang_axial_length.setter
    @enforce_parameter_types
    def housing_rear_overhang_axial_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HousingRearOverhangAxialLength",
            float(value) if value is not None else 0.0,
        )

    @property
    def housing_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HousingThickness")

        if temp is None:
            return 0.0

        return temp

    @housing_thickness.setter
    @enforce_parameter_types
    def housing_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HousingThickness", float(value) if value is not None else 0.0
        )

    @property
    def inner_housing_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerHousingInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def inner_housing_outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerHousingOuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_housing_outer_diameter.setter
    @enforce_parameter_types
    def inner_housing_outer_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerHousingOuterDiameter", value)

    @property
    def maximum_number_of_channels(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfChannels")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_channels(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfChannels")

        if temp is None:
            return 0.0

        return temp

    @number_of_channels.setter
    @enforce_parameter_types
    def number_of_channels(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfChannels", float(value) if value is not None else 0.0
        )

    @property
    def number_of_parallel_flow_paths(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfParallelFlowPaths")

        if temp is None:
            return 0

        return temp

    @number_of_parallel_flow_paths.setter
    @enforce_parameter_types
    def number_of_parallel_flow_paths(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfParallelFlowPaths",
            int(value) if value is not None else 0,
        )

    @property
    def outer_housing_inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterHousingInnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_housing_inner_diameter.setter
    @enforce_parameter_types
    def outer_housing_inner_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterHousingInnerDiameter", value)

    @property
    def outer_housing_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterHousingOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_channel_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalChannelLength")

        if temp is None:
            return 0.0

        return temp

    @property
    def channel(self: "Self") -> "_1454.Channel":
        """mastapy.electric_machines.thermal.Channel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Channel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def front_endcap(self: "Self") -> "_1473.ThermalEndcap":
        """mastapy.electric_machines.thermal.ThermalEndcap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontEndcap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def housing_to_stator_interface_gap(self: "Self") -> "_202.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HousingToStatorInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rear_endcap(self: "Self") -> "_1473.ThermalEndcap":
        """mastapy.electric_machines.thermal.ThermalEndcap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RearEndcap")

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
    def cast_to(self: "Self") -> "_Cast_ThermalHousing":
        """Cast to another type.

        Returns:
            _Cast_ThermalHousing
        """
        return _Cast_ThermalHousing(self)
