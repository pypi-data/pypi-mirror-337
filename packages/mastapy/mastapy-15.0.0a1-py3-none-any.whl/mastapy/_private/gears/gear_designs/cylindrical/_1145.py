"""CylindricalPlanetGearDesign"""

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
from mastapy._private.gears.gear_designs.cylindrical import _1115

_CYLINDRICAL_PLANET_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalPlanetGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _423
    from mastapy._private.gears.gear_designs import _1044, _1045
    from mastapy._private.gears.gear_designs.cylindrical import _1168, _1169
    from mastapy._private.geometry.two_d import _395

    Self = TypeVar("Self", bound="CylindricalPlanetGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearDesign._Cast_CylindricalPlanetGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearDesign:
    """Special nested class for casting CylindricalPlanetGearDesign to subclasses."""

    __parent__: "CylindricalPlanetGearDesign"

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1115.CylindricalGearDesign":
        return self.__parent__._cast(_1115.CylindricalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1044.GearDesign":
        from mastapy._private.gears.gear_designs import _1044

        return self.__parent__._cast(_1044.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1045.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1045

        return self.__parent__._cast(_1045.GearDesignComponent)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearDesign":
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
class CylindricalPlanetGearDesign(_1115.CylindricalGearDesign):
    """CylindricalPlanetGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def has_factorising_annulus(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasFactorisingAnnulus")

        if temp is None:
            return False

        return temp

    @property
    def has_factorising_sun(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasFactorisingSun")

        if temp is None:
            return False

        return temp

    @property
    def internal_external(self: "Self") -> "_395.InternalExternalType":
        """mastapy.geometry.two_d.InternalExternalType"""
        temp = pythonnet_property_get(self.wrapped, "InternalExternal")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.geometry.two_d._395", "InternalExternalType"
        )(value)

    @internal_external.setter
    @enforce_parameter_types
    def internal_external(self: "Self", value: "_395.InternalExternalType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Geometry.TwoD.InternalExternalType"
        )
        pythonnet_property_set(self.wrapped, "InternalExternal", value)

    @property
    def suggested_maximum_number_of_planets(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuggestedMaximumNumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @property
    def planetary_details(self: "Self") -> "_423.PlanetaryDetail":
        """mastapy.gears.PlanetaryDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planet_assembly_indices(self: "Self") -> "List[_1168.NamedPlanetAssemblyIndex]":
        """List[mastapy.gears.gear_designs.cylindrical.NamedPlanetAssemblyIndex]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetAssemblyIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetary_sidebands_amplitude_factors(
        self: "Self",
    ) -> "List[_1169.NamedPlanetSideBandAmplitudeFactor]":
        """List[mastapy.gears.gear_designs.cylindrical.NamedPlanetSideBandAmplitudeFactor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PlanetarySidebandsAmplitudeFactors"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGearDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearDesign
        """
        return _Cast_CylindricalPlanetGearDesign(self)
