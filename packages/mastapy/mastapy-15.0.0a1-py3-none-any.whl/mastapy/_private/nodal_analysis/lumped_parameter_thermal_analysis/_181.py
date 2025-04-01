"""ConvectionFaceBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _213

_CONVECTION_FACE_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ConvectionFaceBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _170,
        _178,
        _180,
        _196,
        _198,
        _201,
        _217,
    )

    Self = TypeVar("Self", bound="ConvectionFaceBase")
    CastSelf = TypeVar("CastSelf", bound="ConvectionFaceBase._Cast_ConvectionFaceBase")


__docformat__ = "restructuredtext en"
__all__ = ("ConvectionFaceBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConvectionFaceBase:
    """Special nested class for casting ConvectionFaceBase to subclasses."""

    __parent__: "ConvectionFaceBase"

    @property
    def thermal_face(self: "CastSelf") -> "_213.ThermalFace":
        return self.__parent__._cast(_213.ThermalFace)

    @property
    def air_gap_convection_face(self: "CastSelf") -> "_170.AirGapConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _170,
        )

        return self.__parent__._cast(_170.AirGapConvectionFace)

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
    def convection_face_base(self: "CastSelf") -> "ConvectionFaceBase":
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
class ConvectionFaceBase(_213.ThermalFace):
    """ConvectionFaceBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVECTION_FACE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def user_defined_heat_transfer_coefficient(
        self: "Self",
    ) -> "_217.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserDefinedHeatTransferCoefficient"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConvectionFaceBase":
        """Cast to another type.

        Returns:
            _Cast_ConvectionFaceBase
        """
        return _Cast_ConvectionFaceBase(self)
