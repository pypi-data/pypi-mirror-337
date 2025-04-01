"""ThermalFace"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ThermalFace"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _170,
        _173,
        _177,
        _178,
        _180,
        _181,
        _183,
        _184,
        _186,
        _188,
        _189,
        _190,
        _194,
        _196,
        _198,
        _201,
        _208,
    )

    Self = TypeVar("Self", bound="ThermalFace")
    CastSelf = TypeVar("CastSelf", bound="ThermalFace._Cast_ThermalFace")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalFace:
    """Special nested class for casting ThermalFace to subclasses."""

    __parent__: "ThermalFace"

    @property
    def air_gap_convection_face(self: "CastSelf") -> "_170.AirGapConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _170,
        )

        return self.__parent__._cast(_170.AirGapConvectionFace)

    @property
    def arbitrary_thermal_face(self: "CastSelf") -> "_173.ArbitraryThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _173,
        )

        return self.__parent__._cast(_173.ArbitraryThermalFace)

    @property
    def capacitive_transport_face(self: "CastSelf") -> "_177.CapacitiveTransportFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _177,
        )

        return self.__parent__._cast(_177.CapacitiveTransportFace)

    @property
    def channel_convection_face(self: "CastSelf") -> "_178.ChannelConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _178,
        )

        return self.__parent__._cast(_178.ChannelConvectionFace)

    @property
    def convection_face(self: "CastSelf") -> "_180.ConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _180,
        )

        return self.__parent__._cast(_180.ConvectionFace)

    @property
    def convection_face_base(self: "CastSelf") -> "_181.ConvectionFaceBase":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _181,
        )

        return self.__parent__._cast(_181.ConvectionFaceBase)

    @property
    def cuboid_thermal_face(self: "CastSelf") -> "_183.CuboidThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _183,
        )

        return self.__parent__._cast(_183.CuboidThermalFace)

    @property
    def cuboid_wall_axial_thermal_face(
        self: "CastSelf",
    ) -> "_184.CuboidWallAxialThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _184,
        )

        return self.__parent__._cast(_184.CuboidWallAxialThermalFace)

    @property
    def cuboid_wall_thermal_face(self: "CastSelf") -> "_186.CuboidWallThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _186,
        )

        return self.__parent__._cast(_186.CuboidWallThermalFace)

    @property
    def cylindrical_axial_thermal_face(
        self: "CastSelf",
    ) -> "_188.CylindricalAxialThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _188,
        )

        return self.__parent__._cast(_188.CylindricalAxialThermalFace)

    @property
    def cylindrical_circumferential_thermal_face(
        self: "CastSelf",
    ) -> "_189.CylindricalCircumferentialThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _189,
        )

        return self.__parent__._cast(_189.CylindricalCircumferentialThermalFace)

    @property
    def cylindrical_radial_thermal_face(
        self: "CastSelf",
    ) -> "_190.CylindricalRadialThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _190,
        )

        return self.__parent__._cast(_190.CylindricalRadialThermalFace)

    @property
    def fe_interface_thermal_face(self: "CastSelf") -> "_194.FEInterfaceThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _194,
        )

        return self.__parent__._cast(_194.FEInterfaceThermalFace)

    @property
    def fluid_channel_cuboid_convection_face(
        self: "CastSelf",
    ) -> "_196.FluidChannelCuboidConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _196,
        )

        return self.__parent__._cast(_196.FluidChannelCuboidConvectionFace)

    @property
    def fluid_channel_cylindrical_radial_convection_face(
        self: "CastSelf",
    ) -> "_198.FluidChannelCylindricalRadialConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _198,
        )

        return self.__parent__._cast(_198.FluidChannelCylindricalRadialConvectionFace)

    @property
    def generic_convection_face(self: "CastSelf") -> "_201.GenericConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _201,
        )

        return self.__parent__._cast(_201.GenericConvectionFace)

    @property
    def sub_fe_interface_thermal_face(
        self: "CastSelf",
    ) -> "_208.SubFEInterfaceThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _208,
        )

        return self.__parent__._cast(_208.SubFEInterfaceThermalFace)

    @property
    def thermal_face(self: "CastSelf") -> "ThermalFace":
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
class ThermalFace(_0.APIBase):
    """ThermalFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def heat_transfer_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatTransferCoefficient")

        if temp is None:
            return 0.0

        return temp

    @heat_transfer_coefficient.setter
    @enforce_parameter_types
    def heat_transfer_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HeatTransferCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    def nusselt_number_calculation_method(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NusseltNumberCalculationMethod")

        if temp is None:
            return ""

        return temp

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
    def cast_to(self: "Self") -> "_Cast_ThermalFace":
        """Cast to another type.

        Returns:
            _Cast_ThermalFace
        """
        return _Cast_ThermalFace(self)
