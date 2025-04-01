"""ChannelConvectionFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _180

_CHANNEL_CONVECTION_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ChannelConvectionFace"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _181,
        _196,
        _198,
        _213,
    )

    Self = TypeVar("Self", bound="ChannelConvectionFace")
    CastSelf = TypeVar(
        "CastSelf", bound="ChannelConvectionFace._Cast_ChannelConvectionFace"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ChannelConvectionFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ChannelConvectionFace:
    """Special nested class for casting ChannelConvectionFace to subclasses."""

    __parent__: "ChannelConvectionFace"

    @property
    def convection_face(self: "CastSelf") -> "_180.ConvectionFace":
        return self.__parent__._cast(_180.ConvectionFace)

    @property
    def convection_face_base(self: "CastSelf") -> "_181.ConvectionFaceBase":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _181,
        )

        return self.__parent__._cast(_181.ConvectionFaceBase)

    @property
    def thermal_face(self: "CastSelf") -> "_213.ThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _213,
        )

        return self.__parent__._cast(_213.ThermalFace)

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
    def channel_convection_face(self: "CastSelf") -> "ChannelConvectionFace":
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
class ChannelConvectionFace(_180.ConvectionFace):
    """ChannelConvectionFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CHANNEL_CONVECTION_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ChannelConvectionFace":
        """Cast to another type.

        Returns:
            _Cast_ChannelConvectionFace
        """
        return _Cast_ChannelConvectionFace(self)
