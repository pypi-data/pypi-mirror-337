"""BevelDifferentialPlanetGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2717

_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2662, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2721,
        _2725,
        _2732,
    )

    Self = TypeVar("Self", bound="BevelDifferentialPlanetGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGear._Cast_BevelDifferentialPlanetGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGear:
    """Special nested class for casting BevelDifferentialPlanetGear to subclasses."""

    __parent__: "BevelDifferentialPlanetGear"

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2717.BevelDifferentialGear":
        return self.__parent__._cast(_2717.BevelDifferentialGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2721.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2721

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
    ) -> "BevelDifferentialPlanetGear":
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
class BevelDifferentialPlanetGear(_2717.BevelDifferentialGear):
    """BevelDifferentialPlanetGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_PLANET_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_planets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @number_of_planets.setter
    @enforce_parameter_types
    def number_of_planets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPlanets", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialPlanetGear":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGear
        """
        return _Cast_BevelDifferentialPlanetGear(self)
