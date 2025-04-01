"""ConicalGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _444

_CONICAL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1329
    from mastapy._private.gears.load_case.conical import _983
    from mastapy._private.gears.rating import _436
    from mastapy._private.gears.rating.agma_gleason_conical import _649
    from mastapy._private.gears.rating.bevel import _638
    from mastapy._private.gears.rating.conical import _629
    from mastapy._private.gears.rating.hypoid import _522
    from mastapy._private.gears.rating.klingelnberg_conical import _495
    from mastapy._private.gears.rating.klingelnberg_hypoid import _492
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _489
    from mastapy._private.gears.rating.spiral_bevel import _486
    from mastapy._private.gears.rating.straight_bevel import _479
    from mastapy._private.gears.rating.straight_bevel_diff import _482
    from mastapy._private.gears.rating.zerol_bevel import _453

    Self = TypeVar("Self", bound="ConicalGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearMeshRating._Cast_ConicalGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshRating:
    """Special nested class for casting ConicalGearMeshRating to subclasses."""

    __parent__: "ConicalGearMeshRating"

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_444.GearMeshRating":
        return self.__parent__._cast(_444.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_436.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _436

        return self.__parent__._cast(_436.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1329.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1329

        return self.__parent__._cast(_1329.AbstractGearMeshAnalysis)

    @property
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_453.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _453

        return self.__parent__._cast(_453.ZerolBevelGearMeshRating)

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
    def conical_gear_mesh_rating(self: "CastSelf") -> "ConicalGearMeshRating":
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
class ConicalGearMeshRating(_444.GearMeshRating):
    """ConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mesh_load_case(self: "Self") -> "_983.ConicalMeshLoadCase":
        """mastapy.gears.load_case.conical.ConicalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_mesh_load_case(self: "Self") -> "_983.ConicalMeshLoadCase":
        """mastapy.gears.load_case.conical.ConicalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def meshed_gears(self: "Self") -> "List[_629.ConicalMeshedGearRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshRating
        """
        return _Cast_ConicalGearMeshRating(self)
