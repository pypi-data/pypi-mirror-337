"""SpringDamperMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5666

_SPRING_DAMPER_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "SpringDamperMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857, _2859, _2863
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7845,
        _7849,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5623,
        _5717,
        _5739,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7787
    from mastapy._private.system_model.part_model.couplings import _2811

    Self = TypeVar("Self", bound="SpringDamperMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpringDamperMultibodyDynamicsAnalysis._Cast_SpringDamperMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperMultibodyDynamicsAnalysis:
    """Special nested class for casting SpringDamperMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "SpringDamperMultibodyDynamicsAnalysis"

    @property
    def coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5666.CouplingMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5666.CouplingMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5739.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5739,
        )

        return self.__parent__._cast(_5739.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5623.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5623,
        )

        return self.__parent__._cast(_5623.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5717.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5717,
        )

        return self.__parent__._cast(_5717.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7849.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7849,
        )

        return self.__parent__._cast(_7849.PartTimeSeriesLoadAnalysisCase)

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
    def spring_damper_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "SpringDamperMultibodyDynamicsAnalysis":
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
class SpringDamperMultibodyDynamicsAnalysis(_5666.CouplingMultibodyDynamicsAnalysis):
    """SpringDamperMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_MULTIBODY_DYNAMICS_ANALYSIS

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
    def assembly_load_case(self: "Self") -> "_7787.SpringDamperLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamperMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperMultibodyDynamicsAnalysis
        """
        return _Cast_SpringDamperMultibodyDynamicsAnalysis(self)
