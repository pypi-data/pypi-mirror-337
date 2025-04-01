"""StraightBevelDiffGearMeshDesign"""

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
from mastapy._private.gears.gear_designs.bevel import _1294

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.StraightBevelDiff",
    "StraightBevelDiffGearMeshDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1045, _1046
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1307
    from mastapy._private.gears.gear_designs.conical import _1268
    from mastapy._private.gears.gear_designs.straight_bevel_diff import (
        _1062,
        _1064,
        _1065,
    )

    Self = TypeVar("Self", bound="StraightBevelDiffGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearMeshDesign._Cast_StraightBevelDiffGearMeshDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearMeshDesign:
    """Special nested class for casting StraightBevelDiffGearMeshDesign to subclasses."""

    __parent__: "StraightBevelDiffGearMeshDesign"

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1294.BevelGearMeshDesign":
        return self.__parent__._cast(_1294.BevelGearMeshDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1307.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1307

        return self.__parent__._cast(_1307.AGMAGleasonConicalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1268.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1268

        return self.__parent__._cast(_1268.ConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_1046.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _1046

        return self.__parent__._cast(_1046.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1045.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1045

        return self.__parent__._cast(_1045.GearDesignComponent)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearMeshDesign":
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
class StraightBevelDiffGearMeshDesign(_1294.BevelGearMeshDesign):
    """StraightBevelDiffGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def pinion_performance_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionPerformanceTorque")

        if temp is None:
            return 0.0

        return temp

    @pinion_performance_torque.setter
    @enforce_parameter_types
    def pinion_performance_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionPerformanceTorque",
            float(value) if value is not None else 0.0,
        )

    @property
    def straight_bevel_diff_gear_set(
        self: "Self",
    ) -> "_1064.StraightBevelDiffGearSetDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def straight_bevel_diff_gears(
        self: "Self",
    ) -> "List[_1062.StraightBevelDiffGearDesign]":
        """List[mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_meshed_gears(
        self: "Self",
    ) -> "List[_1065.StraightBevelDiffMeshedGearDesign]":
        """List[mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffMeshedGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffMeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearMeshDesign
        """
        return _Cast_StraightBevelDiffGearMeshDesign(self)
