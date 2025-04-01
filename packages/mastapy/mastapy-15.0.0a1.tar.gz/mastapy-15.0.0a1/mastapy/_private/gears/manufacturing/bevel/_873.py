"""ConicalGearMicroGeometryConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _874

_CONICAL_GEAR_MICRO_GEOMETRY_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalGearMicroGeometryConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1328, _1331, _1334
    from mastapy._private.gears.manufacturing.bevel import _885

    Self = TypeVar("Self", bound="ConicalGearMicroGeometryConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMicroGeometryConfig._Cast_ConicalGearMicroGeometryConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMicroGeometryConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMicroGeometryConfig:
    """Special nested class for casting ConicalGearMicroGeometryConfig to subclasses."""

    __parent__: "ConicalGearMicroGeometryConfig"

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_874.ConicalGearMicroGeometryConfigBase":
        return self.__parent__._cast(_874.ConicalGearMicroGeometryConfigBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1334.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1334

        return self.__parent__._cast(_1334.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1331.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1331

        return self.__parent__._cast(_1331.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1328.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1328

        return self.__parent__._cast(_1328.AbstractGearAnalysis)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_885.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _885

        return self.__parent__._cast(_885.ConicalPinionMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "ConicalGearMicroGeometryConfig":
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
class ConicalGearMicroGeometryConfig(_874.ConicalGearMicroGeometryConfigBase):
    """ConicalGearMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MICRO_GEOMETRY_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMicroGeometryConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMicroGeometryConfig
        """
        return _Cast_ConicalGearMicroGeometryConfig(self)
