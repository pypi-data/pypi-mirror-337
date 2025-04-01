"""ComponentNodalComposite"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _150

_COMPONENT_NODAL_COMPOSITE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ComponentNodalComposite"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _132,
        _133,
        _134,
        _139,
        _145,
        _151,
        _157,
        _162,
        _163,
        _164,
    )

    Self = TypeVar("Self", bound="ComponentNodalComposite")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentNodalComposite._Cast_ComponentNodalComposite"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentNodalComposite",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentNodalComposite:
    """Special nested class for casting ComponentNodalComposite to subclasses."""

    __parent__: "ComponentNodalComposite"

    @property
    def nodal_composite(self: "CastSelf") -> "_150.NodalComposite":
        return self.__parent__._cast(_150.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_151.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _151

        return self.__parent__._cast(_151.NodalEntity)

    @property
    def bar_elastic_mbd(self: "CastSelf") -> "_132.BarElasticMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _132

        return self.__parent__._cast(_132.BarElasticMBD)

    @property
    def bar_mbd(self: "CastSelf") -> "_133.BarMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _133

        return self.__parent__._cast(_133.BarMBD)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "_134.BarRigidMBD":
        from mastapy._private.nodal_analysis.nodal_entities import _134

        return self.__parent__._cast(_134.BarRigidMBD)

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
    ) -> "_164.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _164

        return self.__parent__._cast(_164.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite(self: "CastSelf") -> "ComponentNodalComposite":
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
class ComponentNodalComposite(_150.NodalComposite):
    """ComponentNodalComposite

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_NODAL_COMPOSITE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentNodalComposite":
        """Cast to another type.

        Returns:
            _Cast_ComponentNodalComposite
        """
        return _Cast_ComponentNodalComposite(self)
