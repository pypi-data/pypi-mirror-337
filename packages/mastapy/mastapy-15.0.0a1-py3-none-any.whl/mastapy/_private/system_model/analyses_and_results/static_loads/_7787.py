"""SpringDamperLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7680

_SPRING_DAMPER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpringDamperLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857, _2859, _2863
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7633,
        _7757,
        _7781,
    )
    from mastapy._private.system_model.part_model.couplings import _2811

    Self = TypeVar("Self", bound="SpringDamperLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="SpringDamperLoadCase._Cast_SpringDamperLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperLoadCase:
    """Special nested class for casting SpringDamperLoadCase to subclasses."""

    __parent__: "SpringDamperLoadCase"

    @property
    def coupling_load_case(self: "CastSelf") -> "_7680.CouplingLoadCase":
        return self.__parent__._cast(_7680.CouplingLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7781.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7781,
        )

        return self.__parent__._cast(_7781.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7633.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7633,
        )

        return self.__parent__._cast(_7633.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7757.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7757,
        )

        return self.__parent__._cast(_7757.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2863.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2863

        return self.__parent__._cast(_2863.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2859.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2859

        return self.__parent__._cast(_2859.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2857.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2857

        return self.__parent__._cast(_2857.DesignEntityAnalysis)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "SpringDamperLoadCase":
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
class SpringDamperLoadCase(_7680.CouplingLoadCase):
    """SpringDamperLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2811.SpringDamper":
        """mastapy.system_model.part_model.couplings.SpringDamper

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamperLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperLoadCase
        """
        return _Cast_SpringDamperLoadCase(self)
