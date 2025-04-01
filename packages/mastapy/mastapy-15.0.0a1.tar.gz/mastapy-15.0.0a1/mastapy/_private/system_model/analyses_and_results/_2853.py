"""CompoundAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _7853
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_COMPOUND_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "CompoundAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Iterable, Type, TypeVar

    from mastapy._private import _7859
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.analyses_and_results import (
        _2864,
        _2865,
        _2866,
        _2867,
        _2868,
        _2869,
        _2870,
        _2871,
        _2872,
        _2873,
        _2874,
        _2875,
        _2876,
        _2877,
        _2878,
        _2879,
        _2880,
        _2881,
        _2882,
        _2883,
        _2884,
        _2885,
        _2886,
        _2887,
        _2888,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7843

    Self = TypeVar("Self", bound="CompoundAnalysis")
    CastSelf = TypeVar("CastSelf", bound="CompoundAnalysis._Cast_CompoundAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("CompoundAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundAnalysis:
    """Special nested class for casting CompoundAnalysis to subclasses."""

    __parent__: "CompoundAnalysis"

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7853.MarshalByRefObjectPermanent":
        return self.__parent__._cast(_7853.MarshalByRefObjectPermanent)

    @property
    def compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_2864.CompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2864

        return self.__parent__._cast(_2864.CompoundAdvancedSystemDeflection)

    @property
    def compound_advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_2865.CompoundAdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2865

        return self.__parent__._cast(_2865.CompoundAdvancedSystemDeflectionSubAnalysis)

    @property
    def compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2866.CompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2866

        return self.__parent__._cast(
            _2866.CompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_2867.CompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2867

        return self.__parent__._cast(_2867.CompoundCriticalSpeedAnalysis)

    @property
    def compound_dynamic_analysis(self: "CastSelf") -> "_2868.CompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2868

        return self.__parent__._cast(_2868.CompoundDynamicAnalysis)

    @property
    def compound_dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2869.CompoundDynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2869

        return self.__parent__._cast(_2869.CompoundDynamicModelAtAStiffness)

    @property
    def compound_dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2870.CompoundDynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2870

        return self.__parent__._cast(_2870.CompoundDynamicModelForHarmonicAnalysis)

    @property
    def compound_dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_2871.CompoundDynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2871

        return self.__parent__._cast(_2871.CompoundDynamicModelForModalAnalysis)

    @property
    def compound_dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_2872.CompoundDynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2872

        return self.__parent__._cast(_2872.CompoundDynamicModelForStabilityAnalysis)

    @property
    def compound_dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_2873.CompoundDynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results import _2873

        return self.__parent__._cast(
            _2873.CompoundDynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2874.CompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2874

        return self.__parent__._cast(_2874.CompoundHarmonicAnalysis)

    @property
    def compound_harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_2875.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results import _2875

        return self.__parent__._cast(
            _2875.CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_2876.CompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results import _2876

        return self.__parent__._cast(_2876.CompoundHarmonicAnalysisOfSingleExcitation)

    @property
    def compound_modal_analysis(self: "CastSelf") -> "_2877.CompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2877

        return self.__parent__._cast(_2877.CompoundModalAnalysis)

    @property
    def compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_2878.CompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2878

        return self.__parent__._cast(_2878.CompoundModalAnalysisAtASpeed)

    @property
    def compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_2879.CompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results import _2879

        return self.__parent__._cast(_2879.CompoundModalAnalysisAtAStiffness)

    @property
    def compound_modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_2880.CompoundModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2880

        return self.__parent__._cast(_2880.CompoundModalAnalysisForHarmonicAnalysis)

    @property
    def compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_2881.CompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2881

        return self.__parent__._cast(_2881.CompoundMultibodyDynamicsAnalysis)

    @property
    def compound_power_flow(self: "CastSelf") -> "_2882.CompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results import _2882

        return self.__parent__._cast(_2882.CompoundPowerFlow)

    @property
    def compound_stability_analysis(
        self: "CastSelf",
    ) -> "_2883.CompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2883

        return self.__parent__._cast(_2883.CompoundStabilityAnalysis)

    @property
    def compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_2884.CompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results import _2884

        return self.__parent__._cast(_2884.CompoundSteadyStateSynchronousResponse)

    @property
    def compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_2885.CompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results import _2885

        return self.__parent__._cast(
            _2885.CompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_2886.CompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results import _2886

        return self.__parent__._cast(
            _2886.CompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def compound_system_deflection(
        self: "CastSelf",
    ) -> "_2887.CompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2887

        return self.__parent__._cast(_2887.CompoundSystemDeflection)

    @property
    def compound_torsional_system_deflection(
        self: "CastSelf",
    ) -> "_2888.CompoundTorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results import _2888

        return self.__parent__._cast(_2888.CompoundTorsionalSystemDeflection)

    @property
    def compound_analysis(self: "CastSelf") -> "CompoundAnalysis":
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
class CompoundAnalysis(_7853.MarshalByRefObjectPermanent):
    """CompoundAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsReady")

        if temp is None:
            return False

        return temp

    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", progress: "_7859.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformAnalysis",
            [_TASK_PROGRESS],
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def results_for(
        self: "Self", design_entity: "_2394.DesignEntity"
    ) -> "Iterable[_7843.DesignEntityCompoundAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.analysis_cases.DesignEntityCompoundAnalysis]

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                self.wrapped,
                "ResultsFor",
                design_entity.wrapped if design_entity else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundAnalysis
        """
        return _Cast_CompoundAnalysis(self)
