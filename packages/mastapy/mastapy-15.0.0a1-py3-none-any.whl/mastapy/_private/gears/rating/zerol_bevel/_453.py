"""ZerolBevelGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel import _638

_ZEROL_BEVEL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.ZerolBevel", "ZerolBevelGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1329
    from mastapy._private.gears.gear_designs.zerol_bevel import _1050
    from mastapy._private.gears.rating import _436, _444
    from mastapy._private.gears.rating.agma_gleason_conical import _649
    from mastapy._private.gears.rating.conical import _623
    from mastapy._private.gears.rating.zerol_bevel import _454

    Self = TypeVar("Self", bound="ZerolBevelGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelGearMeshRating._Cast_ZerolBevelGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearMeshRating:
    """Special nested class for casting ZerolBevelGearMeshRating to subclasses."""

    __parent__: "ZerolBevelGearMeshRating"

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_638.BevelGearMeshRating":
        return self.__parent__._cast(_638.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_649.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _649

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
    def zerol_bevel_gear_mesh_rating(self: "CastSelf") -> "ZerolBevelGearMeshRating":
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
class ZerolBevelGearMeshRating(_638.BevelGearMeshRating):
    """ZerolBevelGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def zerol_bevel_gear_mesh(self: "Self") -> "_1050.ZerolBevelGearMeshDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def zerol_bevel_gear_ratings(self: "Self") -> "List[_454.ZerolBevelGearRating]":
        """List[mastapy.gears.rating.zerol_bevel.ZerolBevelGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearMeshRating
        """
        return _Cast_ZerolBevelGearMeshRating(self)
