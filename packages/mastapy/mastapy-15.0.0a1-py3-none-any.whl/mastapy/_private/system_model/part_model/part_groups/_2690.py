"""ParallelPartGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.part_model.part_groups import _2686

_PARALLEL_PART_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.PartGroups", "ParallelPartGroup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.part_model.part_groups import _2687, _2691, _2692

    Self = TypeVar("Self", bound="ParallelPartGroup")
    CastSelf = TypeVar("CastSelf", bound="ParallelPartGroup._Cast_ParallelPartGroup")


__docformat__ = "restructuredtext en"
__all__ = ("ParallelPartGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParallelPartGroup:
    """Special nested class for casting ParallelPartGroup to subclasses."""

    __parent__: "ParallelPartGroup"

    @property
    def concentric_or_parallel_part_group(
        self: "CastSelf",
    ) -> "_2686.ConcentricOrParallelPartGroup":
        return self.__parent__._cast(_2686.ConcentricOrParallelPartGroup)

    @property
    def part_group(self: "CastSelf") -> "_2692.PartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2692

        return self.__parent__._cast(_2692.PartGroup)

    @property
    def parallel_part_group_selection(
        self: "CastSelf",
    ) -> "_2691.ParallelPartGroupSelection":
        from mastapy._private.system_model.part_model.part_groups import _2691

        return self.__parent__._cast(_2691.ParallelPartGroupSelection)

    @property
    def parallel_part_group(self: "CastSelf") -> "ParallelPartGroup":
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
class ParallelPartGroup(_2686.ConcentricOrParallelPartGroup):
    """ParallelPartGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARALLEL_PART_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_dx_axis_direction(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDXAxisDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def two_dy_axis_direction(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDYAxisDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def two_dz_axis_direction(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDZAxisDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def concentric_part_groups(self: "Self") -> "List[_2687.ConcentricPartGroup]":
        """List[mastapy.system_model.part_model.part_groups.ConcentricPartGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConcentricPartGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ParallelPartGroup":
        """Cast to another type.

        Returns:
            _Cast_ParallelPartGroup
        """
        return _Cast_ParallelPartGroup(self)
