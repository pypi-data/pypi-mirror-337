"""AbstractGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1329

_ABSTRACT_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _444, _449
    from mastapy._private.gears.rating.agma_gleason_conical import _649
    from mastapy._private.gears.rating.bevel import _638
    from mastapy._private.gears.rating.concept import _633, _634
    from mastapy._private.gears.rating.conical import _623, _628
    from mastapy._private.gears.rating.cylindrical import _542, _550
    from mastapy._private.gears.rating.face import _530, _531
    from mastapy._private.gears.rating.hypoid import _522
    from mastapy._private.gears.rating.klingelnberg_conical import _495
    from mastapy._private.gears.rating.klingelnberg_hypoid import _492
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _489
    from mastapy._private.gears.rating.spiral_bevel import _486
    from mastapy._private.gears.rating.straight_bevel import _479
    from mastapy._private.gears.rating.straight_bevel_diff import _482
    from mastapy._private.gears.rating.worm import _457, _461
    from mastapy._private.gears.rating.zerol_bevel import _453

    Self = TypeVar("Self", bound="AbstractGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearMeshRating._Cast_AbstractGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearMeshRating:
    """Special nested class for casting AbstractGearMeshRating to subclasses."""

    __parent__: "AbstractGearMeshRating"

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1329.AbstractGearMeshAnalysis":
        return self.__parent__._cast(_1329.AbstractGearMeshAnalysis)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_444.GearMeshRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.GearMeshRating)

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_449.MeshDutyCycleRating":
        from mastapy._private.gears.rating import _449

        return self.__parent__._cast(_449.MeshDutyCycleRating)

    @property
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_453.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _453

        return self.__parent__._cast(_453.ZerolBevelGearMeshRating)

    @property
    def worm_gear_mesh_rating(self: "CastSelf") -> "_457.WormGearMeshRating":
        from mastapy._private.gears.rating.worm import _457

        return self.__parent__._cast(_457.WormGearMeshRating)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "_461.WormMeshDutyCycleRating":
        from mastapy._private.gears.rating.worm import _461

        return self.__parent__._cast(_461.WormMeshDutyCycleRating)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_479.StraightBevelGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel import _479

        return self.__parent__._cast(_479.StraightBevelGearMeshRating)

    @property
    def straight_bevel_diff_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_482.StraightBevelDiffGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _482

        return self.__parent__._cast(_482.StraightBevelDiffGearMeshRating)

    @property
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_486.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _486

        return self.__parent__._cast(_486.SpiralBevelGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_489.KlingelnbergCycloPalloidSpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _489

        return self.__parent__._cast(
            _489.KlingelnbergCycloPalloidSpiralBevelGearMeshRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_492.KlingelnbergCycloPalloidHypoidGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _492

        return self.__parent__._cast(_492.KlingelnbergCycloPalloidHypoidGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_495.KlingelnbergCycloPalloidConicalGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _495

        return self.__parent__._cast(_495.KlingelnbergCycloPalloidConicalGearMeshRating)

    @property
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "_522.HypoidGearMeshRating":
        from mastapy._private.gears.rating.hypoid import _522

        return self.__parent__._cast(_522.HypoidGearMeshRating)

    @property
    def face_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_530.FaceGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.face import _530

        return self.__parent__._cast(_530.FaceGearMeshDutyCycleRating)

    @property
    def face_gear_mesh_rating(self: "CastSelf") -> "_531.FaceGearMeshRating":
        from mastapy._private.gears.rating.face import _531

        return self.__parent__._cast(_531.FaceGearMeshRating)

    @property
    def cylindrical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_542.CylindricalGearMeshRating":
        from mastapy._private.gears.rating.cylindrical import _542

        return self.__parent__._cast(_542.CylindricalGearMeshRating)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_550.CylindricalMeshDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _550

        return self.__parent__._cast(_550.CylindricalMeshDutyCycleRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_623.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _623

        return self.__parent__._cast(_623.ConicalGearMeshRating)

    @property
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_628.ConicalMeshDutyCycleRating":
        from mastapy._private.gears.rating.conical import _628

        return self.__parent__._cast(_628.ConicalMeshDutyCycleRating)

    @property
    def concept_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_633.ConceptGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.concept import _633

        return self.__parent__._cast(_633.ConceptGearMeshDutyCycleRating)

    @property
    def concept_gear_mesh_rating(self: "CastSelf") -> "_634.ConceptGearMeshRating":
        from mastapy._private.gears.rating.concept import _634

        return self.__parent__._cast(_634.ConceptGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_638.BevelGearMeshRating":
        from mastapy._private.gears.rating.bevel import _638

        return self.__parent__._cast(_638.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_649.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _649

        return self.__parent__._cast(_649.AGMAGleasonConicalGearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "AbstractGearMeshRating":
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
class AbstractGearMeshRating(_1329.AbstractGearMeshAnalysis):
    """AbstractGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def calculated_mesh_efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedMeshEfficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def normalised_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearMeshRating
        """
        return _Cast_AbstractGearMeshRating(self)
