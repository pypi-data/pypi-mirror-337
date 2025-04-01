"""TorsionalFrictionNodePairSimpleLockedStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _162

_TORSIONAL_FRICTION_NODE_PAIR_SIMPLE_LOCKED_STIFFNESS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities",
    "TorsionalFrictionNodePairSimpleLockedStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _138,
        _139,
        _150,
        _151,
        _164,
    )

    Self = TypeVar("Self", bound="TorsionalFrictionNodePairSimpleLockedStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorsionalFrictionNodePairSimpleLockedStiffness._Cast_TorsionalFrictionNodePairSimpleLockedStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorsionalFrictionNodePairSimpleLockedStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorsionalFrictionNodePairSimpleLockedStiffness:
    """Special nested class for casting TorsionalFrictionNodePairSimpleLockedStiffness to subclasses."""

    __parent__: "TorsionalFrictionNodePairSimpleLockedStiffness"

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_162.TorsionalFrictionNodePair":
        return self.__parent__._cast(_162.TorsionalFrictionNodePair)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_139.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.ConcentricConnectionNodalComponent)

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_164.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _164

        return self.__parent__._cast(_164.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_138.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.ComponentNodalComposite)

    @property
    def nodal_composite(self: "CastSelf") -> "_150.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _150

        return self.__parent__._cast(_150.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_151.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _151

        return self.__parent__._cast(_151.NodalEntity)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "TorsionalFrictionNodePairSimpleLockedStiffness":
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
class TorsionalFrictionNodePairSimpleLockedStiffness(_162.TorsionalFrictionNodePair):
    """TorsionalFrictionNodePairSimpleLockedStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORSIONAL_FRICTION_NODE_PAIR_SIMPLE_LOCKED_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorsionalFrictionNodePairSimpleLockedStiffness":
        """Cast to another type.

        Returns:
            _Cast_TorsionalFrictionNodePairSimpleLockedStiffness
        """
        return _Cast_TorsionalFrictionNodePairSimpleLockedStiffness(self)
