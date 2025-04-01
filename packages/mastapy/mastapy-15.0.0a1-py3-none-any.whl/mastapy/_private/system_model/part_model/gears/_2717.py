"""BevelDifferentialGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2721

_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1293
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2662, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2719,
        _2720,
        _2725,
        _2732,
    )

    Self = TypeVar("Self", bound="BevelDifferentialGear")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelDifferentialGear._Cast_BevelDifferentialGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGear:
    """Special nested class for casting BevelDifferentialGear to subclasses."""

    __parent__: "BevelDifferentialGear"

    @property
    def bevel_gear(self: "CastSelf") -> "_2721.BevelGear":
        return self.__parent__._cast(_2721.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2715.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2715

        return self.__parent__._cast(_2715.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2725.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2725

        return self.__parent__._cast(_2725.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2732.Gear":
        from mastapy._private.system_model.part_model.gears import _2732

        return self.__parent__._cast(_2732.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
        from mastapy._private.system_model.part_model import _2662

        return self.__parent__._cast(_2662.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        from mastapy._private.system_model.part_model import _2639

        return self.__parent__._cast(_2639.Component)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2719.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2719

        return self.__parent__._cast(_2719.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2720.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2720

        return self.__parent__._cast(_2720.BevelDifferentialSunGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "BevelDifferentialGear":
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
class BevelDifferentialGear(_2721.BevelGear):
    """BevelDifferentialGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bevel_gear_design(self: "Self") -> "_1293.BevelGearDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGear":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGear
        """
        return _Cast_BevelDifferentialGear(self)
