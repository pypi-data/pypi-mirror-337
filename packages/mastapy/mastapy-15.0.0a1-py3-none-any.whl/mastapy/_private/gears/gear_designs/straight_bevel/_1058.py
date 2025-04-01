"""StraightBevelGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.bevel import _1293

_STRAIGHT_BEVEL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.StraightBevel", "StraightBevelGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1044, _1045
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1306
    from mastapy._private.gears.gear_designs.conical import _1267

    Self = TypeVar("Self", bound="StraightBevelGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="StraightBevelGearDesign._Cast_StraightBevelGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearDesign:
    """Special nested class for casting StraightBevelGearDesign to subclasses."""

    __parent__: "StraightBevelGearDesign"

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1293.BevelGearDesign":
        return self.__parent__._cast(_1293.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1306.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1306

        return self.__parent__._cast(_1306.AGMAGleasonConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1267.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1267

        return self.__parent__._cast(_1267.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1044.GearDesign":
        from mastapy._private.gears.gear_designs import _1044

        return self.__parent__._cast(_1044.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1045.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1045

        return self.__parent__._cast(_1045.GearDesignComponent)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "StraightBevelGearDesign":
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
class StraightBevelGearDesign(_1293.BevelGearDesign):
    """StraightBevelGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearDesign":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearDesign
        """
        return _Cast_StraightBevelGearDesign(self)
