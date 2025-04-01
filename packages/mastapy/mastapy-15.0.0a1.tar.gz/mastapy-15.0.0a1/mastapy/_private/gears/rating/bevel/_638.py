"""BevelGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.agma_gleason_conical import _649

_BEVEL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel", "BevelGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1329
    from mastapy._private.gears.rating import _436, _444
    from mastapy._private.gears.rating.bevel.standards import _642, _644
    from mastapy._private.gears.rating.conical import _623, _629
    from mastapy._private.gears.rating.iso_10300 import _507, _509
    from mastapy._private.gears.rating.spiral_bevel import _486
    from mastapy._private.gears.rating.straight_bevel import _479
    from mastapy._private.gears.rating.zerol_bevel import _453

    Self = TypeVar("Self", bound="BevelGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelGearMeshRating._Cast_BevelGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshRating:
    """Special nested class for casting BevelGearMeshRating to subclasses."""

    __parent__: "BevelGearMeshRating"

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_649.AGMAGleasonConicalGearMeshRating":
        return self.__parent__._cast(_649.AGMAGleasonConicalGearMeshRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_623.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _623

        return self.__parent__._cast(_623.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_444.GearMeshRating":
        from mastapy._private.gears.rating import _444

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
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_486.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _486

        return self.__parent__._cast(_486.SpiralBevelGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "BevelGearMeshRating":
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
class BevelGearMeshRating(_649.AGMAGleasonConicalGearMeshRating):
    """BevelGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def size_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def agma_bevel_mesh_single_flank_rating(
        self: "Self",
    ) -> "_642.AGMASpiralBevelMeshSingleFlankRating":
        """mastapy.gears.rating.bevel.standards.AGMASpiralBevelMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AGMABevelMeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gleason_bevel_mesh_single_flank_rating(
        self: "Self",
    ) -> "_644.GleasonSpiralBevelMeshSingleFlankRating":
        """mastapy.gears.rating.bevel.standards.GleasonSpiralBevelMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GleasonBevelMeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b1(
        self: "Self",
    ) -> "_509.ISO10300MeshSingleFlankRatingMethodB1":
        """mastapy.gears.rating.isoISO10300MeshSingleFlankRatingMethodB1

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO10300BevelMeshSingleFlankRatingMethodB1"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b2(
        self: "Self",
    ) -> "_507.ISO10300MeshSingleFlankRatingBevelMethodB2":
        """mastapy.gears.rating.isoISO10300MeshSingleFlankRatingBevelMethodB2

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISO10300BevelMeshSingleFlankRatingMethodB2"
        )

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
    def gears_in_mesh(self: "Self") -> "List[_629.ConicalMeshedGearRating]":
        """List[mastapy.gears.rating.conical.ConicalMeshedGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsInMesh")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshRating
        """
        return _Cast_BevelGearMeshRating(self)
