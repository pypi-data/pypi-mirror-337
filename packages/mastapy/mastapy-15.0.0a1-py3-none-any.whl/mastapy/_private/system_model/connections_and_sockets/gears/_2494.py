"""BevelGearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets.gears import _2490

_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1294
    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.connections_and_sockets import _2463, _2472
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2492,
        _2498,
        _2504,
        _2514,
        _2516,
        _2518,
        _2522,
    )

    Self = TypeVar("Self", bound="BevelGearMesh")
    CastSelf = TypeVar("CastSelf", bound="BevelGearMesh._Cast_BevelGearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMesh:
    """Special nested class for casting BevelGearMesh to subclasses."""

    __parent__: "BevelGearMesh"

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2490.AGMAGleasonConicalGearMesh":
        return self.__parent__._cast(_2490.AGMAGleasonConicalGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2498.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2498

        return self.__parent__._cast(_2498.ConicalGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2504.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2504

        return self.__parent__._cast(_2504.GearMesh)

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
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2492.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2492

        return self.__parent__._cast(_2492.BevelDifferentialGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2514.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2514

        return self.__parent__._cast(_2514.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2516.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2516

        return self.__parent__._cast(_2516.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2518.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2518

        return self.__parent__._cast(_2518.StraightBevelGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2522.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.ZerolBevelGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "BevelGearMesh":
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
class BevelGearMesh(_2490.AGMAGleasonConicalGearMesh):
    """BevelGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_mesh_design(self: "Self") -> "_1294.BevelGearMeshDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gear_mesh_design(self: "Self") -> "_1294.BevelGearMeshDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMesh":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMesh
        """
        return _Cast_BevelGearMesh(self)
