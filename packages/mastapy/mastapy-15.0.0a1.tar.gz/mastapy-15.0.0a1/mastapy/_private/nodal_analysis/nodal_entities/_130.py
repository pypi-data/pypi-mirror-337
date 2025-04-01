"""ArbitraryNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _149

_ARBITRARY_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ArbitraryNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _136,
        _137,
        _144,
        _148,
        _151,
        _159,
    )

    Self = TypeVar("Self", bound="ArbitraryNodalComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="ArbitraryNodalComponent._Cast_ArbitraryNodalComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ArbitraryNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ArbitraryNodalComponent:
    """Special nested class for casting ArbitraryNodalComponent to subclasses."""

    __parent__: "ArbitraryNodalComponent"

    @property
    def nodal_component(self: "CastSelf") -> "_149.NodalComponent":
        return self.__parent__._cast(_149.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_151.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _151

        return self.__parent__._cast(_151.NodalEntity)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_136.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _136

        return self.__parent__._cast(_136.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_137.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _137

        return self.__parent__._cast(_137.CMSNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_144.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.GearMeshNodePair)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_148.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.LineContactStiffnessEntity)

    @property
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_159.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _159

        return self.__parent__._cast(_159.SurfaceToSurfaceContactStiffnessEntity)

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "ArbitraryNodalComponent":
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
class ArbitraryNodalComponent(_149.NodalComponent):
    """ArbitraryNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ARBITRARY_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ArbitraryNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_ArbitraryNodalComponent
        """
        return _Cast_ArbitraryNodalComponent(self)
