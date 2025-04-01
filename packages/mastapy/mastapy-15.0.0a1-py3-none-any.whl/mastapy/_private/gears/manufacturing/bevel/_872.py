"""ConicalGearManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.bevel import _874

_CONICAL_GEAR_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalGearManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1328, _1331, _1334
    from mastapy._private.gears.manufacturing.bevel import _884, _890

    Self = TypeVar("Self", bound="ConicalGearManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearManufacturingConfig._Cast_ConicalGearManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearManufacturingConfig:
    """Special nested class for casting ConicalGearManufacturingConfig to subclasses."""

    __parent__: "ConicalGearManufacturingConfig"

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
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_884.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _884

        return self.__parent__._cast(_884.ConicalPinionManufacturingConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_890.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _890

        return self.__parent__._cast(_890.ConicalWheelManufacturingConfig)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalGearManufacturingConfig":
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
class ConicalGearManufacturingConfig(_874.ConicalGearMicroGeometryConfigBase):
    """ConicalGearManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearManufacturingConfig
        """
        return _Cast_ConicalGearManufacturingConfig(self)
