"""CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4398,
)

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2857
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7839,
        _7843,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4303
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4430,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2529

    Self = TypeVar(
        "Self", bound="CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow._Cast_CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow:
    """Special nested class for casting CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4398.AbstractShaftToMountableComponentConnectionCompoundPowerFlow":
        return self.__parent__._cast(
            _4398.AbstractShaftToMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4430.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4430,
        )

        return self.__parent__._cast(_4430.ConnectionCompoundPowerFlow)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7839.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7839,
        )

        return self.__parent__._cast(_7839.ConnectionCompoundAnalysis)

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
    def cycloidal_disc_planetary_bearing_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow":
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
class CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow(
    _4398.AbstractShaftToMountableComponentConnectionCompoundPowerFlow
):
    """CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(
        self: "Self",
    ) -> "_2529.CycloidalDiscPlanetaryBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(
        self: "Self",
    ) -> "_2529.CycloidalDiscPlanetaryBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4303.CycloidalDiscPlanetaryBearingConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CycloidalDiscPlanetaryBearingConnectionPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4303.CycloidalDiscPlanetaryBearingConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CycloidalDiscPlanetaryBearingConnectionPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow
        """
        return _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow(self)
