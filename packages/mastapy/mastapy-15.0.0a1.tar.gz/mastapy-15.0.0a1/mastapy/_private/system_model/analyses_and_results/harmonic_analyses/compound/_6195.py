"""ExternalCADModelCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6168,
)

_EXTERNAL_CAD_MODEL_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ExternalCADModelCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7843,
        _7846,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6001,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6224,
    )
    from mastapy._private.system_model.part_model import _2648

    Self = TypeVar("Self", bound="ExternalCADModelCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalCADModelCompoundHarmonicAnalysis._Cast_ExternalCADModelCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelCompoundHarmonicAnalysis:
    """Special nested class for casting ExternalCADModelCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ExternalCADModelCompoundHarmonicAnalysis"

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6168.ComponentCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6168.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6224.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6224,
        )

        return self.__parent__._cast(_6224.PartCompoundHarmonicAnalysis)

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
    def external_cad_model_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ExternalCADModelCompoundHarmonicAnalysis":
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
class ExternalCADModelCompoundHarmonicAnalysis(_6168.ComponentCompoundHarmonicAnalysis):
    """ExternalCADModelCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_CAD_MODEL_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2648.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

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
    ) -> "List[_6001.ExternalCADModelHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ExternalCADModelHarmonicAnalysis]

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
    ) -> "List[_6001.ExternalCADModelHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ExternalCADModelHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ExternalCADModelCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelCompoundHarmonicAnalysis
        """
        return _Cast_ExternalCADModelCompoundHarmonicAnalysis(self)
