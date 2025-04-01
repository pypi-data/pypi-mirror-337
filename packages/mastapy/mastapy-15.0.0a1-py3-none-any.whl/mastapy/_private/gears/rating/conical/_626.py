"""ConicalGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _447

_CONICAL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1330
    from mastapy._private.gears.gear_designs import _1040
    from mastapy._private.gears.rating import _438
    from mastapy._private.gears.rating.agma_gleason_conical import _651
    from mastapy._private.gears.rating.bevel import _640
    from mastapy._private.gears.rating.hypoid import _524
    from mastapy._private.gears.rating.klingelnberg_conical import _497
    from mastapy._private.gears.rating.klingelnberg_hypoid import _494
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _491
    from mastapy._private.gears.rating.spiral_bevel import _488
    from mastapy._private.gears.rating.straight_bevel import _481
    from mastapy._private.gears.rating.straight_bevel_diff import _484
    from mastapy._private.gears.rating.zerol_bevel import _455

    Self = TypeVar("Self", bound="ConicalGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearSetRating._Cast_ConicalGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetRating:
    """Special nested class for casting ConicalGearSetRating to subclasses."""

    __parent__: "ConicalGearSetRating"

    @property
    def gear_set_rating(self: "CastSelf") -> "_447.GearSetRating":
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
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_484.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _484

        return self.__parent__._cast(_484.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_488.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _488

        return self.__parent__._cast(_488.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_491.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _491

        return self.__parent__._cast(
            _491.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_494.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _494

        return self.__parent__._cast(_494.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_497.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _497

        return self.__parent__._cast(_497.KlingelnbergCycloPalloidConicalGearSetRating)

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
    ) -> "_651.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _651

        return self.__parent__._cast(_651.AGMAGleasonConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "ConicalGearSetRating":
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
class ConicalGearSetRating(_447.GearSetRating):
    """ConicalGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating_settings(self: "Self") -> "_1040.BevelHypoidGearRatingSettingsItem":
        """mastapy.gears.gear_designs.BevelHypoidGearRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetRating
        """
        return _Cast_ConicalGearSetRating(self)
