"""PlanetaryGearSetCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3108,
)

_PLANETARY_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "PlanetaryGearSetCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7843,
        _7846,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3059,
        _3120,
        _3141,
        _3161,
    )

    Self = TypeVar("Self", bound="PlanetaryGearSetCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryGearSetCompoundSystemDeflection._Cast_PlanetaryGearSetCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSetCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSetCompoundSystemDeflection:
    """Special nested class for casting PlanetaryGearSetCompoundSystemDeflection to subclasses."""

    __parent__: "PlanetaryGearSetCompoundSystemDeflection"

    @property
    def cylindrical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3108.CylindricalGearSetCompoundSystemDeflection":
        return self.__parent__._cast(_3108.CylindricalGearSetCompoundSystemDeflection)

    @property
    def gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3120.GearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3120,
        )

        return self.__parent__._cast(_3120.GearSetCompoundSystemDeflection)

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3161.SpecialisedAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3161,
        )

        return self.__parent__._cast(_3161.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3059.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3059,
        )

        return self.__parent__._cast(_3059.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3141.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3141,
        )

        return self.__parent__._cast(_3141.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7846.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7846,
        )

        return self.__parent__._cast(_7846.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7843.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7843,
        )

        return self.__parent__._cast(_7843.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2857.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2857

        return self.__parent__._cast(_2857.DesignEntityAnalysis)

    @property
    def planetary_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "PlanetaryGearSetCompoundSystemDeflection":
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
class PlanetaryGearSetCompoundSystemDeflection(
    _3108.CylindricalGearSetCompoundSystemDeflection
):
    """PlanetaryGearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSetCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSetCompoundSystemDeflection
        """
        return _Cast_PlanetaryGearSetCompoundSystemDeflection(self)
