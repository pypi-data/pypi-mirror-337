"""Connection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2394

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2456,
        _2459,
        _2460,
        _2464,
        _2472,
        _2478,
        _2483,
        _2486,
        _2487,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2533,
        _2535,
        _2537,
        _2539,
        _2541,
        _2543,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2526,
        _2529,
        _2532,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2490,
        _2492,
        _2494,
        _2496,
        _2498,
        _2500,
        _2502,
        _2504,
        _2506,
        _2509,
        _2510,
        _2511,
        _2514,
        _2516,
        _2518,
        _2520,
        _2522,
    )
    from mastapy._private.system_model.part_model import _2639

    Self = TypeVar("Self", bound="Connection")
    CastSelf = TypeVar("CastSelf", bound="Connection._Cast_Connection")


__docformat__ = "restructuredtext en"
__all__ = ("Connection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Connection:
    """Special nested class for casting Connection to subclasses."""

    __parent__: "Connection"

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2456.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2456

        return self.__parent__._cast(_2456.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2459.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2459

        return self.__parent__._cast(_2459.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2460.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2460

        return self.__parent__._cast(_2460.CoaxialConnection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2464.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2464

        return self.__parent__._cast(_2464.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2472.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2472

        return self.__parent__._cast(_2472.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2478.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2478

        return self.__parent__._cast(_2478.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2483.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2483

        return self.__parent__._cast(_2483.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2486.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2486

        return self.__parent__._cast(_2486.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2490.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2490

        return self.__parent__._cast(_2490.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2492.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2492

        return self.__parent__._cast(_2492.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2494.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2494

        return self.__parent__._cast(_2494.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2496.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2496

        return self.__parent__._cast(_2496.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2498.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2498

        return self.__parent__._cast(_2498.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2500.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2500

        return self.__parent__._cast(_2500.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2502.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2502

        return self.__parent__._cast(_2502.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2504.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2504

        return self.__parent__._cast(_2504.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2506.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2506

        return self.__parent__._cast(_2506.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2509.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2509

        return self.__parent__._cast(_2509.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2510.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2510

        return self.__parent__._cast(_2510.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2511.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2511

        return self.__parent__._cast(_2511.KlingelnbergCycloPalloidSpiralBevelGearMesh)

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
    def worm_gear_mesh(self: "CastSelf") -> "_2520.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2520

        return self.__parent__._cast(_2520.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2522.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2526.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2526,
        )

        return self.__parent__._cast(_2526.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2529.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2529,
        )

        return self.__parent__._cast(_2529.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2532.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2532,
        )

        return self.__parent__._cast(_2532.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2533.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2533,
        )

        return self.__parent__._cast(_2533.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2535.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2535,
        )

        return self.__parent__._cast(_2535.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2537.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2537,
        )

        return self.__parent__._cast(_2537.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2539.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2539,
        )

        return self.__parent__._cast(_2539.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2541.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2541,
        )

        return self.__parent__._cast(_2541.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2543.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2543,
        )

        return self.__parent__._cast(_2543.TorqueConverterConnection)

    @property
    def connection(self: "CastSelf") -> "Connection":
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
class Connection(_2394.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionID")

        if temp is None:
            return ""

        return temp

    @property
    def drawing_position(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DrawingPosition")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @drawing_position.setter
    @enforce_parameter_types
    def drawing_position(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "DrawingPosition", value)

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def speed_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def owner_a(self: "Self") -> "_2639.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def owner_b(self: "Self") -> "_2639.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_a(self: "Self") -> "_2487.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_b(self: "Self") -> "_2487.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def other_owner(self: "Self", component: "_2639.Component") -> "_2639.Component":
        """mastapy.system_model.part_model.Component

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "OtherOwner", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket_for_component(
        self: "Self", component: "_2639.Component"
    ) -> "_2487.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "OtherSocket",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket(self: "Self", socket: "_2487.Socket") -> "_2487.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "OtherSocket", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def socket_for(self: "Self", component: "_2639.Component") -> "_2487.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "SocketFor", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Connection":
        """Cast to another type.

        Returns:
            _Cast_Connection
        """
        return _Cast_Connection(self)
