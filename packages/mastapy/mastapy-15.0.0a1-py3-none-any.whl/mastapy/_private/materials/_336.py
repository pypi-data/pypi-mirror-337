"""Fluid"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.databases import _2011
from mastapy._private.utility.units_and_measurements.measurements import (
    _1807,
    _1828,
    _1839,
    _1888,
)

_FLUID = python_net_import("SMT.MastaAPI.Materials", "Fluid")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _370

    Self = TypeVar("Self", bound="Fluid")
    CastSelf = TypeVar("CastSelf", bound="Fluid._Cast_Fluid")


__docformat__ = "restructuredtext en"
__all__ = ("Fluid",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Fluid:
    """Special nested class for casting Fluid to subclasses."""

    __parent__: "Fluid"

    @property
    def named_database_item(self: "CastSelf") -> "_2011.NamedDatabaseItem":
        return self.__parent__._cast(_2011.NamedDatabaseItem)

    @property
    def fluid(self: "CastSelf") -> "Fluid":
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
class Fluid(_2011.NamedDatabaseItem):
    """Fluid

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLUID

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def density_vs_temperature(
        self: "Self",
    ) -> "_370.TemperatureDependentProperty[_1807.Density]":
        """mastapy.materials.TemperatureDependentProperty[mastapy.utility.units_and_measurements.measurements.Density]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DensityVsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1807.Density](temp)

    @property
    def heat_conductivity_vs_temperature(
        self: "Self",
    ) -> "_370.TemperatureDependentProperty[_1828.HeatConductivity]":
        """mastapy.materials.TemperatureDependentProperty[mastapy.utility.units_and_measurements.measurements.HeatConductivity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatConductivityVsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1828.HeatConductivity](
            temp
        )

    @property
    def kinematic_viscosity_vs_temperature(
        self: "Self",
    ) -> "_370.TemperatureDependentProperty[_1839.KinematicViscosity]":
        """mastapy.materials.TemperatureDependentProperty[mastapy.utility.units_and_measurements.measurements.KinematicViscosity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosityVsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1839.KinematicViscosity](
            temp
        )

    @property
    def specific_heat_capacity_vs_temperature(
        self: "Self",
    ) -> "_370.TemperatureDependentProperty[_1888.SpecificHeat]":
        """mastapy.materials.TemperatureDependentProperty[mastapy.utility.units_and_measurements.measurements.SpecificHeat]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificHeatCapacityVsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1888.SpecificHeat](temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Fluid":
        """Cast to another type.

        Returns:
            _Cast_Fluid
        """
        return _Cast_Fluid(self)
