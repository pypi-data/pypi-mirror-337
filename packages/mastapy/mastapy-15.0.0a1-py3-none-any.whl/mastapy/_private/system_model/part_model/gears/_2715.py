"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2725

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2662, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2717,
        _2719,
        _2720,
        _2721,
        _2732,
        _2736,
        _2746,
        _2748,
        _2750,
        _2752,
        _2753,
        _2756,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2725.ConicalGear":
        return self.__parent__._cast(_2725.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2732.Gear":
        from mastapy._private.system_model.part_model.gears import _2732

        return self.__parent__._cast(_2732.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
        from mastapy._private.system_model.part_model import _2662

        return self.__parent__._cast(_2662.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        from mastapy._private.system_model.part_model import _2639

        return self.__parent__._cast(_2639.Component)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2717.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2717

        return self.__parent__._cast(_2717.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2719.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2719

        return self.__parent__._cast(_2719.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2720.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2720

        return self.__parent__._cast(_2720.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2721.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2721

        return self.__parent__._cast(_2721.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2736.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2736

        return self.__parent__._cast(_2736.HypoidGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2746.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2746

        return self.__parent__._cast(_2746.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2748.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2748

        return self.__parent__._cast(_2748.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2750.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2752.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2753.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2753

        return self.__parent__._cast(_2753.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2756.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
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
class AGMAGleasonConicalGear(_2725.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
