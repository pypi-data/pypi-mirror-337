"""ConceptGearSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3254,
)

_CONCEPT_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "ConceptGearSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857, _2859, _2863
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7845,
        _7848,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7668
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3218,
        _3273,
        _3275,
    )
    from mastapy._private.system_model.part_model.gears import _2723

    Self = TypeVar("Self", bound="ConceptGearSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearSteadyStateSynchronousResponse._Cast_ConceptGearSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSteadyStateSynchronousResponse:
    """Special nested class for casting ConceptGearSteadyStateSynchronousResponse to subclasses."""

    __parent__: "ConceptGearSteadyStateSynchronousResponse"

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3254.GearSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3254.GearSteadyStateSynchronousResponse)

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3273.MountableComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3273,
        )

        return self.__parent__._cast(
            _3273.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3218.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3218,
        )

        return self.__parent__._cast(_3218.ComponentSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3275.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3275,
        )

        return self.__parent__._cast(_3275.PartSteadyStateSynchronousResponse)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7848.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7848,
        )

        return self.__parent__._cast(_7848.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7845.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7845,
        )

        return self.__parent__._cast(_7845.PartAnalysisCase)

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
    def concept_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ConceptGearSteadyStateSynchronousResponse":
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
class ConceptGearSteadyStateSynchronousResponse(
    _3254.GearSteadyStateSynchronousResponse
):
    """ConceptGearSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2723.ConceptGear":
        """mastapy.system_model.part_model.gears.ConceptGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7668.ConceptGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSteadyStateSynchronousResponse
        """
        return _Cast_ConceptGearSteadyStateSynchronousResponse(self)
