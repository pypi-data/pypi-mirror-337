"""ConicalGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _445

_CONICAL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1328
    from mastapy._private.gears.rating import _437, _442
    from mastapy._private.gears.rating.agma_gleason_conical import _650
    from mastapy._private.gears.rating.bevel import _639
    from mastapy._private.gears.rating.hypoid import _523
    from mastapy._private.gears.rating.klingelnberg_conical import _496
    from mastapy._private.gears.rating.klingelnberg_hypoid import _493
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _490
    from mastapy._private.gears.rating.spiral_bevel import _487
    from mastapy._private.gears.rating.straight_bevel import _480
    from mastapy._private.gears.rating.straight_bevel_diff import _483
    from mastapy._private.gears.rating.zerol_bevel import _454

    Self = TypeVar("Self", bound="ConicalGearRating")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearRating._Cast_ConicalGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearRating:
    """Special nested class for casting ConicalGearRating to subclasses."""

    __parent__: "ConicalGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_445.GearRating":
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
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_483.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _483

        return self.__parent__._cast(_483.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_487.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _487

        return self.__parent__._cast(_487.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_490.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _490

        return self.__parent__._cast(_490.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_493.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _493

        return self.__parent__._cast(_493.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_496.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _496

        return self.__parent__._cast(_496.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_523.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _523

        return self.__parent__._cast(_523.HypoidGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_639.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _639

        return self.__parent__._cast(_639.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_650.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _650

        return self.__parent__._cast(_650.AGMAGleasonConicalGearRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "ConicalGearRating":
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
class ConicalGearRating(_445.GearRating):
    """ConicalGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def concave_flank_rating(self: "Self") -> "_442.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConcaveFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def convex_flank_rating(self: "Self") -> "_442.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConvexFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearRating
        """
        return _Cast_ConicalGearRating(self)
