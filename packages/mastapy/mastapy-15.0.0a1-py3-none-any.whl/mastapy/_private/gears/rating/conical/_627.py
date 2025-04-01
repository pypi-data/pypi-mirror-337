"""ConicalGearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _448

_CONICAL_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.bevel.standards import _641, _643, _645
    from mastapy._private.gears.rating.hypoid.standards import _526
    from mastapy._private.gears.rating.iso_10300 import _513, _514, _515, _516, _517

    Self = TypeVar("Self", bound="ConicalGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSingleFlankRating._Cast_ConicalGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSingleFlankRating:
    """Special nested class for casting ConicalGearSingleFlankRating to subclasses."""

    __parent__: "ConicalGearSingleFlankRating"

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_448.GearSingleFlankRating":
        return self.__parent__._cast(_448.GearSingleFlankRating)

    @property
    def iso10300_single_flank_rating(
        self: "CastSelf",
    ) -> "_513.ISO10300SingleFlankRating":
        from mastapy._private.gears.rating.iso_10300 import _513

        return self.__parent__._cast(_513.ISO10300SingleFlankRating)

    @property
    def iso10300_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_514.ISO10300SingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _514

        return self.__parent__._cast(_514.ISO10300SingleFlankRatingBevelMethodB2)

    @property
    def iso10300_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_515.ISO10300SingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _515

        return self.__parent__._cast(_515.ISO10300SingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_516.ISO10300SingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _516

        return self.__parent__._cast(_516.ISO10300SingleFlankRatingMethodB1)

    @property
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_517.ISO10300SingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _517

        return self.__parent__._cast(_517.ISO10300SingleFlankRatingMethodB2)

    @property
    def gleason_hypoid_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_526.GleasonHypoidGearSingleFlankRating":
        from mastapy._private.gears.rating.hypoid.standards import _526

        return self.__parent__._cast(_526.GleasonHypoidGearSingleFlankRating)

    @property
    def agma_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_641.AGMASpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _641

        return self.__parent__._cast(_641.AGMASpiralBevelGearSingleFlankRating)

    @property
    def gleason_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_643.GleasonSpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _643

        return self.__parent__._cast(_643.GleasonSpiralBevelGearSingleFlankRating)

    @property
    def spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_645.SpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _645

        return self.__parent__._cast(_645.SpiralBevelGearSingleFlankRating)

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ConicalGearSingleFlankRating":
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
class ConicalGearSingleFlankRating(_448.GearSingleFlankRating):
    """ConicalGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSingleFlankRating
        """
        return _Cast_ConicalGearSingleFlankRating(self)
