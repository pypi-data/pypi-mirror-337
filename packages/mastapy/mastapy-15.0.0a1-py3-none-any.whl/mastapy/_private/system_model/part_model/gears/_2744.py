"""PlanetaryGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2728

_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1170
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2629, _2666, _2676
    from mastapy._private.system_model.part_model.gears import _2727, _2729, _2734

    Self = TypeVar("Self", bound="PlanetaryGearSet")
    CastSelf = TypeVar("CastSelf", bound="PlanetaryGearSet._Cast_PlanetaryGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSet:
    """Special nested class for casting PlanetaryGearSet to subclasses."""

    __parent__: "PlanetaryGearSet"

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2728.CylindricalGearSet":
        return self.__parent__._cast(_2728.CylindricalGearSet)

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
    def planetary_gear_set(self: "CastSelf") -> "PlanetaryGearSet":
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
class PlanetaryGearSet(_2728.CylindricalGearSet):
    """PlanetaryGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def phase_requirement(self: "Self") -> "_1170.PlanetGearSetPhaseRequirement":
        """mastapy.gears.gear_designs.cylindrical.PlanetGearSetPhaseRequirement"""
        temp = pythonnet_property_get(self.wrapped, "PhaseRequirement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.PlanetGearSetPhaseRequirement",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1170",
            "PlanetGearSetPhaseRequirement",
        )(value)

    @phase_requirement.setter
    @enforce_parameter_types
    def phase_requirement(
        self: "Self", value: "_1170.PlanetGearSetPhaseRequirement"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.PlanetGearSetPhaseRequirement",
        )
        pythonnet_property_set(self.wrapped, "PhaseRequirement", value)

    @property
    def annuluses(self: "Self") -> "List[_2727.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Annuluses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planets(self: "Self") -> "List[_2729.CylindricalPlanetGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def suns(self: "Self") -> "List[_2727.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Suns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_annulus(self: "Self") -> "_2727.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddAnnulus")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def add_planet(self: "Self") -> "_2727.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddPlanet")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def add_sun(self: "Self") -> "_2727.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddSun")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def set_number_of_planets(self: "Self", amount: "int") -> None:
        """Method does not return.

        Args:
            amount (int)
        """
        amount = int(amount)
        pythonnet_method_call(
            self.wrapped, "SetNumberOfPlanets", amount if amount else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSet":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSet
        """
        return _Cast_PlanetaryGearSet(self)
