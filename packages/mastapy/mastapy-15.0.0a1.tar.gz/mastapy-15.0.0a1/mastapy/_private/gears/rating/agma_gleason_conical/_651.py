"""AGMAGleasonConicalGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _626

_AGMA_GLEASON_CONICAL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.AGMAGleasonConical", "AGMAGleasonConicalGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1330
    from mastapy._private.gears.rating import _438, _447
    from mastapy._private.gears.rating.bevel import _640
    from mastapy._private.gears.rating.hypoid import _524
    from mastapy._private.gears.rating.spiral_bevel import _488
    from mastapy._private.gears.rating.straight_bevel import _481
    from mastapy._private.gears.rating.zerol_bevel import _455

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetRating._Cast_AGMAGleasonConicalGearSetRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetRating:
    """Special nested class for casting AGMAGleasonConicalGearSetRating to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetRating"

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_626.ConicalGearSetRating":
        return self.__parent__._cast(_626.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_447.GearSetRating":
        from mastapy._private.gears.rating import _447

        return self.__parent__._cast(_447.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_438.AbstractGearSetRating":
        from mastapy._private.gears.rating import _438

        return self.__parent__._cast(_438.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1330.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1330

        return self.__parent__._cast(_1330.AbstractGearSetAnalysis)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_455.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _455

        return self.__parent__._cast(_455.ZerolBevelGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_481.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _481

        return self.__parent__._cast(_481.StraightBevelGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_488.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _488

        return self.__parent__._cast(_488.SpiralBevelGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_524.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _524

        return self.__parent__._cast(_524.HypoidGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_640.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _640

        return self.__parent__._cast(_640.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetRating":
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
class AGMAGleasonConicalGearSetRating(_626.ConicalGearSetRating):
    """AGMAGleasonConicalGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetRating
        """
        return _Cast_AGMAGleasonConicalGearSetRating(self)
