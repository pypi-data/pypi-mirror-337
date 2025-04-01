"""Gear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2662

_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1044
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2717,
        _2719,
        _2720,
        _2721,
        _2723,
        _2725,
        _2727,
        _2729,
        _2730,
        _2734,
        _2736,
        _2738,
        _2740,
        _2742,
        _2746,
        _2748,
        _2750,
        _2752,
        _2753,
        _2754,
        _2756,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2682

    Self = TypeVar("Self", bound="Gear")
    CastSelf = TypeVar("CastSelf", bound="Gear._Cast_Gear")


__docformat__ = "restructuredtext en"
__all__ = ("Gear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Gear:
    """Special nested class for casting Gear to subclasses."""

    __parent__: "Gear"

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
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
    def concept_gear(self: "CastSelf") -> "_2723.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2723

        return self.__parent__._cast(_2723.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2725.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2725

        return self.__parent__._cast(_2725.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2727.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2727

        return self.__parent__._cast(_2727.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2729.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2729

        return self.__parent__._cast(_2729.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2730.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2730

        return self.__parent__._cast(_2730.FaceGear)

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
    def worm_gear(self: "CastSelf") -> "_2754.WormGear":
        from mastapy._private.system_model.part_model.gears import _2754

        return self.__parent__._cast(_2754.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2756.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.ZerolBevelGear)

    @property
    def gear(self: "CastSelf") -> "Gear":
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
class Gear(_2662.MountableComponent):
    """Gear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cloned_from(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClonedFrom")

        if temp is None:
            return ""

        return temp

    @property
    def even_number_of_teeth_required(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EvenNumberOfTeethRequired")

        if temp is None:
            return False

        return temp

    @even_number_of_teeth_required.setter
    @enforce_parameter_types
    def even_number_of_teeth_required(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvenNumberOfTeethRequired",
            bool(value) if value is not None else False,
        )

    @property
    def is_clone_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsCloneGear")

        if temp is None:
            return False

        return temp

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def maximum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth.setter
    @enforce_parameter_types
    def maximum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def maximum_and_minimum_number_of_teeth_deviation(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation"
        )

        if temp is None:
            return None

        return temp

    @maximum_and_minimum_number_of_teeth_deviation.setter
    @enforce_parameter_types
    def maximum_and_minimum_number_of_teeth_deviation(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation", value
        )

    @property
    def minimum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth.setter
    @enforce_parameter_types
    def minimum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def active_gear_design(self: "Self") -> "_1044.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def gear_set(self: "Self") -> "_2734.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def shaft(self: "Self") -> "_2682.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def connect_to(self: "Self", other_gear: "Gear") -> None:
        """Method does not return.

        Args:
            other_gear (mastapy.system_model.part_model.gears.Gear)
        """
        pythonnet_method_call(
            self.wrapped, "ConnectTo", other_gear.wrapped if other_gear else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Gear":
        """Cast to another type.

        Returns:
            _Cast_Gear
        """
        return _Cast_Gear(self)
