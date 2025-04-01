"""PlanetBasedFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2620

_PLANET_BASED_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "PlanetBasedFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2613, _2617, _2621, _2623

    Self = TypeVar("Self", bound="PlanetBasedFELink")
    CastSelf = TypeVar("CastSelf", bound="PlanetBasedFELink._Cast_PlanetBasedFELink")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetBasedFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetBasedFELink:
    """Special nested class for casting PlanetBasedFELink to subclasses."""

    __parent__: "PlanetBasedFELink"

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2620.MultiNodeFELink":
        return self.__parent__._cast(_2620.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2613.FELink":
        from mastapy._private.system_model.fe.links import _2613

        return self.__parent__._cast(_2613.FELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2617.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2617

        return self.__parent__._cast(_2617.GearWithDuplicatedMeshesFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2621.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2621

        return self.__parent__._cast(_2621.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2623.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2623

        return self.__parent__._cast(_2623.PlanetCarrierFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "PlanetBasedFELink":
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
class PlanetBasedFELink(_2620.MultiNodeFELink):
    """PlanetBasedFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_BASED_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetBasedFELink":
        """Cast to another type.

        Returns:
            _Cast_PlanetBasedFELink
        """
        return _Cast_PlanetBasedFELink(self)
