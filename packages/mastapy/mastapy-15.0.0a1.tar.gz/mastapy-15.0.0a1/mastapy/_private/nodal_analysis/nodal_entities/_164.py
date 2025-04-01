"""TwoBodyConnectionNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _138

_TWO_BODY_CONNECTION_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "TwoBodyConnectionNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _139,
        _145,
        _150,
        _151,
        _157,
        _162,
        _163,
    )

    Self = TypeVar("Self", bound="TwoBodyConnectionNodalComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoBodyConnectionNodalComponent._Cast_TwoBodyConnectionNodalComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoBodyConnectionNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoBodyConnectionNodalComponent:
    """Special nested class for casting TwoBodyConnectionNodalComponent to subclasses."""

    __parent__: "TwoBodyConnectionNodalComponent"

    @property
    def component_nodal_composite(self: "CastSelf") -> "_138.ComponentNodalComposite":
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
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "_139.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.ConcentricConnectionNodalComponent)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_145.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _145

        return self.__parent__._cast(_145.GearMeshPointOnFlankContact)

    @property
    def simple_bar(self: "CastSelf") -> "_157.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _157

        return self.__parent__._cast(_157.SimpleBar)

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_162.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _162

        return self.__parent__._cast(_162.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_163.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _163

        return self.__parent__._cast(
            _163.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "TwoBodyConnectionNodalComponent":
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
class TwoBodyConnectionNodalComponent(_138.ComponentNodalComposite):
    """TwoBodyConnectionNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_BODY_CONNECTION_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TwoBodyConnectionNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_TwoBodyConnectionNodalComponent
        """
        return _Cast_TwoBodyConnectionNodalComponent(self)
