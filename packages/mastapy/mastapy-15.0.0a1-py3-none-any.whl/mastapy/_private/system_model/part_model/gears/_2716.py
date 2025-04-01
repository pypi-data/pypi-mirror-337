"""AGMAGleasonConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2726

_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2629, _2666, _2676
    from mastapy._private.system_model.part_model.gears import (
        _2718,
        _2722,
        _2734,
        _2737,
        _2747,
        _2749,
        _2751,
        _2757,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSet:
    """Special nested class for casting AGMAGleasonConicalGearSet to subclasses."""

    __parent__: "AGMAGleasonConicalGearSet"

    @property
    def conical_gear_set(self: "CastSelf") -> "_2726.ConicalGearSet":
        return self.__parent__._cast(_2726.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2734.GearSet":
        from mastapy._private.system_model.part_model.gears import _2734

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
    def agma_gleason_conical_gear_set(self: "CastSelf") -> "AGMAGleasonConicalGearSet":
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
class AGMAGleasonConicalGearSet(_2726.ConicalGearSet):
    """AGMAGleasonConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSet
        """
        return _Cast_AGMAGleasonConicalGearSet(self)
