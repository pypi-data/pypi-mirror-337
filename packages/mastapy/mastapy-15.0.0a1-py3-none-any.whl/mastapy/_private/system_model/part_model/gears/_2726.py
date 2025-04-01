"""ConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2734

_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1269
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2629, _2666, _2676
    from mastapy._private.system_model.part_model.gears import (
        _2716,
        _2718,
        _2722,
        _2725,
        _2737,
        _2739,
        _2741,
        _2743,
        _2747,
        _2749,
        _2751,
        _2757,
    )

    Self = TypeVar("Self", bound="ConicalGearSet")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearSet._Cast_ConicalGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSet:
    """Special nested class for casting ConicalGearSet to subclasses."""

    __parent__: "ConicalGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2734.GearSet":
        return self.__parent__._cast(_2734.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2676.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2676

        return self.__parent__._cast(_2676.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2629.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2629

        return self.__parent__._cast(_2629.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2716.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2716

        return self.__parent__._cast(_2716.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2718.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2718

        return self.__parent__._cast(_2718.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2722.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2722

        return self.__parent__._cast(_2722.BevelGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2737.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2737

        return self.__parent__._cast(_2737.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2739.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2739

        return self.__parent__._cast(_2739.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2741.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2741

        return self.__parent__._cast(_2741.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2743.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2743

        return self.__parent__._cast(_2743.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2747.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2747

        return self.__parent__._cast(_2747.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2749.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2749

        return self.__parent__._cast(_2749.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2751.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.StraightBevelGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2757.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.ZerolBevelGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "ConicalGearSet":
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
class ConicalGearSet(_2734.GearSet):
    """ConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_set_design(self: "Self") -> "_1269.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_set_design(self: "Self") -> "_1269.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears(self: "Self") -> "List[_2725.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSet
        """
        return _Cast_ConicalGearSet(self)
