"""ConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2732

_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1267
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2662, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2717,
        _2719,
        _2720,
        _2721,
        _2733,
        _2736,
        _2738,
        _2740,
        _2742,
        _2746,
        _2748,
        _2750,
        _2752,
        _2753,
        _2756,
    )

    Self = TypeVar("Self", bound="ConicalGear")
    CastSelf = TypeVar("CastSelf", bound="ConicalGear._Cast_ConicalGear")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGear:
    """Special nested class for casting ConicalGear to subclasses."""

    __parent__: "ConicalGear"

    @property
    def gear(self: "CastSelf") -> "_2732.Gear":
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
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2715.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2715

        return self.__parent__._cast(_2715.AGMAGleasonConicalGear)

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
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2738.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2738

        return self.__parent__._cast(_2738.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2740.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2740

        return self.__parent__._cast(_2740.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2742.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2742

        return self.__parent__._cast(_2742.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def conical_gear(self: "CastSelf") -> "ConicalGear":
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
class ConicalGear(_2732.Gear):
    """ConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    def orientation(self: "Self") -> "_2733.GearOrientations":
        """mastapy.system_model.part_model.gears.GearOrientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.gears._2733", "GearOrientations"
        )(value)

    @orientation.setter
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2733.GearOrientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    def active_gear_design(self: "Self") -> "_1267.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_design(self: "Self") -> "_1267.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGear":
        """Cast to another type.

        Returns:
            _Cast_ConicalGear
        """
        return _Cast_ConicalGear(self)
