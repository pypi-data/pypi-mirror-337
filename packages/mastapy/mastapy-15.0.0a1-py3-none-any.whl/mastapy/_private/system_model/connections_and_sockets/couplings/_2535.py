"""ConceptCouplingConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.couplings import _2537

_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.connections_and_sockets import _2463, _2472

    Self = TypeVar("Self", bound="ConceptCouplingConnection")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptCouplingConnection._Cast_ConceptCouplingConnection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptCouplingConnection:
    """Special nested class for casting ConceptCouplingConnection to subclasses."""

    __parent__: "ConceptCouplingConnection"

    @property
    def coupling_connection(self: "CastSelf") -> "_2537.CouplingConnection":
        return self.__parent__._cast(_2537.CouplingConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2472.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2472

        return self.__parent__._cast(_2472.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2463.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2463

        return self.__parent__._cast(_2463.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def concept_coupling_connection(self: "CastSelf") -> "ConceptCouplingConnection":
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
class ConceptCouplingConnection(_2537.CouplingConnection):
    """ConceptCouplingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_COUPLING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptCouplingConnection":
        """Cast to another type.

        Returns:
            _Cast_ConceptCouplingConnection
        """
        return _Cast_ConceptCouplingConnection(self)
