"""ThermalElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ThermalElement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.thermal import _1460
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _171,
        _172,
        _182,
        _185,
        _191,
        _193,
        _197,
        _199,
        _200,
    )

    Self = TypeVar("Self", bound="ThermalElement")
    CastSelf = TypeVar("CastSelf", bound="ThermalElement._Cast_ThermalElement")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalElement:
    """Special nested class for casting ThermalElement to subclasses."""

    __parent__: "ThermalElement"

    @property
    def air_gap_thermal_element(self: "CastSelf") -> "_171.AirGapThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _171,
        )

        return self.__parent__._cast(_171.AirGapThermalElement)

    @property
    def arbitrary_thermal_element(self: "CastSelf") -> "_172.ArbitraryThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _172,
        )

        return self.__parent__._cast(_172.ArbitraryThermalElement)

    @property
    def cuboid_thermal_element(self: "CastSelf") -> "_182.CuboidThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _182,
        )

        return self.__parent__._cast(_182.CuboidThermalElement)

    @property
    def cuboid_wall_thermal_element(
        self: "CastSelf",
    ) -> "_185.CuboidWallThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _185,
        )

        return self.__parent__._cast(_185.CuboidWallThermalElement)

    @property
    def cylindrical_thermal_element(
        self: "CastSelf",
    ) -> "_191.CylindricalThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _191,
        )

        return self.__parent__._cast(_191.CylindricalThermalElement)

    @property
    def fe_interface_thermal_element(
        self: "CastSelf",
    ) -> "_193.FEInterfaceThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _193,
        )

        return self.__parent__._cast(_193.FEInterfaceThermalElement)

    @property
    def fluid_channel_cuboid_element(
        self: "CastSelf",
    ) -> "_197.FluidChannelCuboidElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _197,
        )

        return self.__parent__._cast(_197.FluidChannelCuboidElement)

    @property
    def fluid_channel_cylindrical_radial_element(
        self: "CastSelf",
    ) -> "_199.FluidChannelCylindricalRadialElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _199,
        )

        return self.__parent__._cast(_199.FluidChannelCylindricalRadialElement)

    @property
    def fluid_channel_element(self: "CastSelf") -> "_200.FluidChannelElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _200,
        )

        return self.__parent__._cast(_200.FluidChannelElement)

    @property
    def end_winding_thermal_element(
        self: "CastSelf",
    ) -> "_1460.EndWindingThermalElement":
        from mastapy._private.electric_machines.thermal import _1460

        return self.__parent__._cast(_1460.EndWindingThermalElement)

    @property
    def thermal_element(self: "CastSelf") -> "ThermalElement":
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
class ThermalElement(_0.APIBase):
    """ThermalElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_ThermalElement":
        """Cast to another type.

        Returns:
            _Cast_ThermalElement
        """
        return _Cast_ThermalElement(self)
