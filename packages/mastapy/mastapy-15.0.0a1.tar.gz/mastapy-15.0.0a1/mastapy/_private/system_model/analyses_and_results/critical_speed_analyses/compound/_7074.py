"""UnbalancedMassCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7075,
)

_UNBALANCED_MASS_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "UnbalancedMassCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7843,
        _7846,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6943,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6976,
        _7030,
        _7032,
    )
    from mastapy._private.system_model.part_model import _2677

    Self = TypeVar("Self", bound="UnbalancedMassCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UnbalancedMassCompoundCriticalSpeedAnalysis._Cast_UnbalancedMassCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UnbalancedMassCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UnbalancedMassCompoundCriticalSpeedAnalysis:
    """Special nested class for casting UnbalancedMassCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "UnbalancedMassCompoundCriticalSpeedAnalysis"

    @property
    def virtual_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7075.VirtualComponentCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _7075.VirtualComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7030.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7030,
        )

        return self.__parent__._cast(
            _7030.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6976.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6976,
        )

        return self.__parent__._cast(_6976.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7032.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7032,
        )

        return self.__parent__._cast(_7032.PartCompoundCriticalSpeedAnalysis)

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
    def unbalanced_mass_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "UnbalancedMassCompoundCriticalSpeedAnalysis":
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
class UnbalancedMassCompoundCriticalSpeedAnalysis(
    _7075.VirtualComponentCompoundCriticalSpeedAnalysis
):
    """UnbalancedMassCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UNBALANCED_MASS_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2677.UnbalancedMass":
        """mastapy.system_model.part_model.UnbalancedMass

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6943.UnbalancedMassCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.UnbalancedMassCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6943.UnbalancedMassCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.UnbalancedMassCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_UnbalancedMassCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_UnbalancedMassCompoundCriticalSpeedAnalysis
        """
        return _Cast_UnbalancedMassCompoundCriticalSpeedAnalysis(self)
