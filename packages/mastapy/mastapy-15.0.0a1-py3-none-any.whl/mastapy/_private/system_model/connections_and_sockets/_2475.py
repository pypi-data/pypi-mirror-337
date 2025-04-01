"""MountableComponentSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2467

_MOUNTABLE_COMPONENT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "MountableComponentSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2457,
        _2458,
        _2473,
        _2474,
        _2487,
    )

    Self = TypeVar("Self", bound="MountableComponentSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="MountableComponentSocket._Cast_MountableComponentSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentSocket:
    """Special nested class for casting MountableComponentSocket to subclasses."""

    __parent__: "MountableComponentSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2467.CylindricalSocket":
        return self.__parent__._cast(_2467.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2487.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2487

        return self.__parent__._cast(_2487.Socket)

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2457.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2457

        return self.__parent__._cast(_2457.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2458.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2458

        return self.__parent__._cast(_2458.BearingOuterSocket)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2473.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2473

        return self.__parent__._cast(_2473.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2474.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2474

        return self.__parent__._cast(_2474.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(self: "CastSelf") -> "MountableComponentSocket":
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
class MountableComponentSocket(_2467.CylindricalSocket):
    """MountableComponentSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentSocket":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentSocket
        """
        return _Cast_MountableComponentSocket(self)
