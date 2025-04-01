"""CouplingConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4052

_COUPLING_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "CouplingConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2855, _2857, _2859
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7838,
        _7841,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4006,
        _4011,
        _4020,
        _4069,
        _4091,
        _4109,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2537

    Self = TypeVar("Self", bound="CouplingConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionStabilityAnalysis._Cast_CouplingConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionStabilityAnalysis:
    """Special nested class for casting CouplingConnectionStabilityAnalysis to subclasses."""

    __parent__: "CouplingConnectionStabilityAnalysis"

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.InterMountableComponentConnectionStabilityAnalysis":
        return self.__parent__._cast(
            _4052.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4020,
        )

        return self.__parent__._cast(_4020.ConnectionStabilityAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7841.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7841,
        )

        return self.__parent__._cast(_7841.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7838.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7838,
        )

        return self.__parent__._cast(_7838.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2855.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2855

        return self.__parent__._cast(_2855.ConnectionAnalysis)

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
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4006.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4006,
        )

        return self.__parent__._cast(_4006.ClutchConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4011.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4011,
        )

        return self.__parent__._cast(_4011.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4069.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4069,
        )

        return self.__parent__._cast(
            _4069.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4091.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4091,
        )

        return self.__parent__._cast(_4091.SpringDamperConnectionStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4109.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4109,
        )

        return self.__parent__._cast(_4109.TorqueConverterConnectionStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionStabilityAnalysis":
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
class CouplingConnectionStabilityAnalysis(
    _4052.InterMountableComponentConnectionStabilityAnalysis
):
    """CouplingConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2537.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionStabilityAnalysis
        """
        return _Cast_CouplingConnectionStabilityAnalysis(self)
