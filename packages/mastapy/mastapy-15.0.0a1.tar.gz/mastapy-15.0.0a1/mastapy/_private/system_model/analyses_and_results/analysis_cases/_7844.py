"""FEAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7850

_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "FEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2856
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7356,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7835
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6599,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5987,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4860
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5148,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4038,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3245,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3033,
        _3040,
    )

    Self = TypeVar("Self", bound="FEAnalysis")
    CastSelf = TypeVar("CastSelf", bound="FEAnalysis._Cast_FEAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("FEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEAnalysis:
    """Special nested class for casting FEAnalysis to subclasses."""

    __parent__: "FEAnalysis"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7850.StaticLoadAnalysisCase":
        return self.__parent__._cast(_7850.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7835.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7835,
        )

        return self.__parent__._cast(_7835.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2856.Context":
        from mastapy._private.system_model.analyses_and_results import _2856

        return self.__parent__._cast(_2856.Context)

    @property
    def system_deflection(self: "CastSelf") -> "_3033.SystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3033,
        )

        return self.__parent__._cast(_3033.SystemDeflection)

    @property
    def torsional_system_deflection(
        self: "CastSelf",
    ) -> "_3040.TorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3040,
        )

        return self.__parent__._cast(_3040.TorsionalSystemDeflection)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3245.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3245,
        )

        return self.__parent__._cast(
            _3245.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4038,
        )

        return self.__parent__._cast(_4038.DynamicModelForStabilityAnalysis)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4860.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4860,
        )

        return self.__parent__._cast(_4860.DynamicModelForModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5148.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5148,
        )

        return self.__parent__._cast(_5148.DynamicModelAtAStiffness)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5987.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5987,
        )

        return self.__parent__._cast(_5987.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6599.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6599,
        )

        return self.__parent__._cast(_6599.DynamicAnalysis)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7356.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7356,
        )

        return self.__parent__._cast(_7356.AdvancedSystemDeflectionSubAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "FEAnalysis":
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
class FEAnalysis(_7850.StaticLoadAnalysisCase):
    """FEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def stiffness_with_respect_to_input_power_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StiffnessWithRespectToInputPowerLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_at_zero_displacement_for_input_power_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueAtZeroDisplacementForInputPowerLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_to_output(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioToOutput")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FEAnalysis
        """
        return _Cast_FEAnalysis(self)
