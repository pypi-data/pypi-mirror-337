"""RootAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model import _2628

_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.geometry import _392
    from mastapy._private.system_model import _2391, _2394
    from mastapy._private.system_model.part_model import _2629, _2666
    from mastapy._private.system_model.part_model.part_groups import _2690
    from mastapy._private.system_model.part_model.projections import _2685

    Self = TypeVar("Self", bound="RootAssembly")
    CastSelf = TypeVar("CastSelf", bound="RootAssembly._Cast_RootAssembly")


__docformat__ = "restructuredtext en"
__all__ = ("RootAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssembly:
    """Special nested class for casting RootAssembly to subclasses."""

    __parent__: "RootAssembly"

    @property
    def assembly(self: "CastSelf") -> "_2628.Assembly":
        return self.__parent__._cast(_2628.Assembly)

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
    def root_assembly(self: "CastSelf") -> "RootAssembly":
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
class RootAssembly(_2628.Assembly):
    """RootAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def model(self: "Self") -> "_2391.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def packaging_limits(self: "Self") -> "_392.PackagingLimits":
        """mastapy.geometry.PackagingLimits

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PackagingLimits")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def parallel_part_groups(self: "Self") -> "List[_2690.ParallelPartGroup]":
        """List[mastapy.system_model.part_model.part_groups.ParallelPartGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParallelPartGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def parallel_part_groups_drawing_order(
        self: "Self",
    ) -> "List[_2685.SpecifiedParallelPartGroupDrawingOrder]":
        """List[mastapy.system_model.part_model.projections.SpecifiedParallelPartGroupDrawingOrder]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParallelPartGroupsDrawingOrder")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def attempt_to_fix_all_cylindrical_gear_sets_by_changing_normal_module(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "AttemptToFixAllCylindricalGearSetsByChangingNormalModule"
        )

    def attempt_to_fix_all_gear_sets(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AttemptToFixAllGearSets")

    def open_fe_substructure_version_comparer(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "OpenFESubstructureVersionComparer")

    def set_packaging_limits_to_current_bounding_box(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetPackagingLimitsToCurrentBoundingBox")

    def set_packaging_limits_to_current_bounding_box_of_all_gears(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "SetPackagingLimitsToCurrentBoundingBoxOfAllGears"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssembly":
        """Cast to another type.

        Returns:
            _Cast_RootAssembly
        """
        return _Cast_RootAssembly(self)
