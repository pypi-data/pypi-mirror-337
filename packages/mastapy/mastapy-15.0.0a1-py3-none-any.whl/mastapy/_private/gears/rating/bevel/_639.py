"""BevelGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.agma_gleason_conical import _650

_BEVEL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel", "BevelGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1328
    from mastapy._private.gears.rating import _437, _445
    from mastapy._private.gears.rating.conical import _624
    from mastapy._private.gears.rating.spiral_bevel import _487
    from mastapy._private.gears.rating.straight_bevel import _480
    from mastapy._private.gears.rating.zerol_bevel import _454

    Self = TypeVar("Self", bound="BevelGearRating")
    CastSelf = TypeVar("CastSelf", bound="BevelGearRating._Cast_BevelGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearRating:
    """Special nested class for casting BevelGearRating to subclasses."""

    __parent__: "BevelGearRating"

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_650.AGMAGleasonConicalGearRating":
        return self.__parent__._cast(_650.AGMAGleasonConicalGearRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_624.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _624

        return self.__parent__._cast(_624.ConicalGearRating)

    @property
    def gear_rating(self: "CastSelf") -> "_445.GearRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_437.AbstractGearRating":
        from mastapy._private.gears.rating import _437

        return self.__parent__._cast(_437.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1328.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1328

        return self.__parent__._cast(_1328.AbstractGearAnalysis)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_454.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _454

        return self.__parent__._cast(_454.ZerolBevelGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_480.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _480

        return self.__parent__._cast(_480.StraightBevelGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_487.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _487

        return self.__parent__._cast(_487.SpiralBevelGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "BevelGearRating":
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
class BevelGearRating(_650.AGMAGleasonConicalGearRating):
    """BevelGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearRating":
        """Cast to another type.

        Returns:
            _Cast_BevelGearRating
        """
        return _Cast_BevelGearRating(self)
