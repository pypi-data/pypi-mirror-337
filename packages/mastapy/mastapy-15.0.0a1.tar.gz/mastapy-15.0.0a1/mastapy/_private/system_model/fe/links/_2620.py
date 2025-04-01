"""MultiNodeFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2613

_MULTI_NODE_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "MultiNodeFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import (
        _2614,
        _2616,
        _2617,
        _2618,
        _2619,
        _2621,
        _2622,
        _2623,
        _2624,
        _2625,
        _2626,
    )

    Self = TypeVar("Self", bound="MultiNodeFELink")
    CastSelf = TypeVar("CastSelf", bound="MultiNodeFELink._Cast_MultiNodeFELink")


__docformat__ = "restructuredtext en"
__all__ = ("MultiNodeFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultiNodeFELink:
    """Special nested class for casting MultiNodeFELink to subclasses."""

    __parent__: "MultiNodeFELink"

    @property
    def fe_link(self: "CastSelf") -> "_2613.FELink":
        return self.__parent__._cast(_2613.FELink)

    @property
    def electric_machine_stator_fe_link(
        self: "CastSelf",
    ) -> "_2614.ElectricMachineStatorFELink":
        from mastapy._private.system_model.fe.links import _2614

        return self.__parent__._cast(_2614.ElectricMachineStatorFELink)

    @property
    def gear_mesh_fe_link(self: "CastSelf") -> "_2616.GearMeshFELink":
        from mastapy._private.system_model.fe.links import _2616

        return self.__parent__._cast(_2616.GearMeshFELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2617.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2617

        return self.__parent__._cast(_2617.GearWithDuplicatedMeshesFELink)

    @property
    def multi_angle_connection_fe_link(
        self: "CastSelf",
    ) -> "_2618.MultiAngleConnectionFELink":
        from mastapy._private.system_model.fe.links import _2618

        return self.__parent__._cast(_2618.MultiAngleConnectionFELink)

    @property
    def multi_node_connector_fe_link(
        self: "CastSelf",
    ) -> "_2619.MultiNodeConnectorFELink":
        from mastapy._private.system_model.fe.links import _2619

        return self.__parent__._cast(_2619.MultiNodeConnectorFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2621.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2621

        return self.__parent__._cast(_2621.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "_2622.PlanetBasedFELink":
        from mastapy._private.system_model.fe.links import _2622

        return self.__parent__._cast(_2622.PlanetBasedFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2623.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2623

        return self.__parent__._cast(_2623.PlanetCarrierFELink)

    @property
    def point_load_fe_link(self: "CastSelf") -> "_2624.PointLoadFELink":
        from mastapy._private.system_model.fe.links import _2624

        return self.__parent__._cast(_2624.PointLoadFELink)

    @property
    def rolling_ring_connection_fe_link(
        self: "CastSelf",
    ) -> "_2625.RollingRingConnectionFELink":
        from mastapy._private.system_model.fe.links import _2625

        return self.__parent__._cast(_2625.RollingRingConnectionFELink)

    @property
    def shaft_hub_connection_fe_link(
        self: "CastSelf",
    ) -> "_2626.ShaftHubConnectionFELink":
        from mastapy._private.system_model.fe.links import _2626

        return self.__parent__._cast(_2626.ShaftHubConnectionFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "MultiNodeFELink":
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
class MultiNodeFELink(_2613.FELink):
    """MultiNodeFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTI_NODE_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MultiNodeFELink":
        """Cast to another type.

        Returns:
            _Cast_MultiNodeFELink
        """
        return _Cast_MultiNodeFELink(self)
