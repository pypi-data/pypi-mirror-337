"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2629

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2638, _2650, _2661, _2666
    from mastapy._private.system_model.part_model.couplings import (
        _2780,
        _2782,
        _2785,
        _2788,
        _2791,
        _2793,
        _2804,
        _2811,
        _2813,
        _2818,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2771
    from mastapy._private.system_model.part_model.gears import (
        _2716,
        _2718,
        _2722,
        _2724,
        _2726,
        _2728,
        _2731,
        _2734,
        _2737,
        _2739,
        _2741,
        _2743,
        _2744,
        _2747,
        _2749,
        _2751,
        _2755,
        _2757,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2629.AbstractAssembly":
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
    def bolted_joint(self: "CastSelf") -> "_2638.BoltedJoint":
        from mastapy._private.system_model.part_model import _2638

        return self.__parent__._cast(_2638.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2650.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2650

        return self.__parent__._cast(_2650.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2661.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2661

        return self.__parent__._cast(_2661.MicrophoneArray)

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
    def concept_gear_set(self: "CastSelf") -> "_2724.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2724

        return self.__parent__._cast(_2724.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2726.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2726

        return self.__parent__._cast(_2726.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2728.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2728

        return self.__parent__._cast(_2728.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2731.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2731

        return self.__parent__._cast(_2731.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2734.GearSet":
        from mastapy._private.system_model.part_model.gears import _2734

        return self.__parent__._cast(_2734.GearSet)

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
    def planetary_gear_set(self: "CastSelf") -> "_2744.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2744

        return self.__parent__._cast(_2744.PlanetaryGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2755.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2757.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2771.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2771

        return self.__parent__._cast(_2771.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2780.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2780

        return self.__parent__._cast(_2780.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2782.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2782

        return self.__parent__._cast(_2782.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2785.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2785

        return self.__parent__._cast(_2785.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2788.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2788

        return self.__parent__._cast(_2788.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2791.CVT":
        from mastapy._private.system_model.part_model.couplings import _2791

        return self.__parent__._cast(_2791.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2793.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2793

        return self.__parent__._cast(_2793.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2804.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2804

        return self.__parent__._cast(_2804.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2811.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2811

        return self.__parent__._cast(_2811.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2813.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2813

        return self.__parent__._cast(_2813.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2818.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2629.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
