"""ShaftToMountableComponentConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2456

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.connections_and_sockets import (
        _2460,
        _2463,
        _2478,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2526

    Self = TypeVar("Self", bound="ShaftToMountableComponentConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnection._Cast_ShaftToMountableComponentConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnection:
    """Special nested class for casting ShaftToMountableComponentConnection to subclasses."""

    __parent__: "ShaftToMountableComponentConnection"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2456.AbstractShaftToMountableComponentConnection":
        return self.__parent__._cast(_2456.AbstractShaftToMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2463.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2463

        return self.__parent__._cast(_2463.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2460.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2460

        return self.__parent__._cast(_2460.CoaxialConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2478.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2478

        return self.__parent__._cast(_2478.PlanetaryConnection)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2526.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2526,
        )

        return self.__parent__._cast(_2526.CycloidalDiscCentralBearingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnection":
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
class ShaftToMountableComponentConnection(
    _2456.AbstractShaftToMountableComponentConnection
):
    """ShaftToMountableComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftToMountableComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnection
        """
        return _Cast_ShaftToMountableComponentConnection(self)
