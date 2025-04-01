"""BevelDifferentialGearMeshModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4823

_BEVEL_DIFFERENTIAL_GEAR_MESH_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "BevelDifferentialGearMeshModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2855, _2857, _2859
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7838,
        _7841,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4811,
        _4839,
        _4842,
        _4870,
        _4877,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7650
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2907,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2492

    Self = TypeVar("Self", bound="BevelDifferentialGearMeshModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearMeshModalAnalysis._Cast_BevelDifferentialGearMeshModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearMeshModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearMeshModalAnalysis:
    """Special nested class for casting BevelDifferentialGearMeshModalAnalysis to subclasses."""

    __parent__: "BevelDifferentialGearMeshModalAnalysis"

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4823.BevelGearMeshModalAnalysis":
        return self.__parent__._cast(_4823.BevelGearMeshModalAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4811.AGMAGleasonConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4811,
        )

        return self.__parent__._cast(_4811.AGMAGleasonConicalGearMeshModalAnalysis)

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4839.ConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4839,
        )

        return self.__parent__._cast(_4839.ConicalGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4870.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4870,
        )

        return self.__parent__._cast(_4870.GearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4877.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4877,
        )

        return self.__parent__._cast(
            _4877.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4842.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4842,
        )

        return self.__parent__._cast(_4842.ConnectionModalAnalysis)

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
    def bevel_differential_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "BevelDifferentialGearMeshModalAnalysis":
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
class BevelDifferentialGearMeshModalAnalysis(_4823.BevelGearMeshModalAnalysis):
    """BevelDifferentialGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_MESH_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2492.BevelDifferentialGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7650.BevelDifferentialGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2907.BevelDifferentialGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearMeshModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearMeshModalAnalysis
        """
        return _Cast_BevelDifferentialGearMeshModalAnalysis(self)
