"""OilSealPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4294

_OIL_SEAL_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "OilSealPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857, _2859, _2863
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7845,
        _7848,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4283,
        _4340,
        _4342,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7755
    from mastapy._private.system_model.part_model import _2664

    Self = TypeVar("Self", bound="OilSealPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="OilSealPowerFlow._Cast_OilSealPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("OilSealPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilSealPowerFlow:
    """Special nested class for casting OilSealPowerFlow to subclasses."""

    __parent__: "OilSealPowerFlow"

    @property
    def connector_power_flow(self: "CastSelf") -> "_4294.ConnectorPowerFlow":
        return self.__parent__._cast(_4294.ConnectorPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4340.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4340

        return self.__parent__._cast(_4340.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4283.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4283

        return self.__parent__._cast(_4283.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4342.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4342

        return self.__parent__._cast(_4342.PartPowerFlow)

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
    def oil_seal_power_flow(self: "CastSelf") -> "OilSealPowerFlow":
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
class OilSealPowerFlow(_4294.ConnectorPowerFlow):
    """OilSealPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_SEAL_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2664.OilSeal":
        """mastapy.system_model.part_model.OilSeal

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7755.OilSealLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_OilSealPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_OilSealPowerFlow
        """
        return _Cast_OilSealPowerFlow(self)
