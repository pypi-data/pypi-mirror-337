"""Socket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2457,
        _2458,
        _2463,
        _2465,
        _2467,
        _2469,
        _2470,
        _2471,
        _2473,
        _2474,
        _2475,
        _2476,
        _2477,
        _2479,
        _2480,
        _2481,
        _2484,
        _2485,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2534,
        _2536,
        _2538,
        _2540,
        _2542,
        _2544,
        _2545,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2524,
        _2525,
        _2527,
        _2528,
        _2530,
        _2531,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2491,
        _2493,
        _2495,
        _2497,
        _2499,
        _2501,
        _2503,
        _2505,
        _2507,
        _2508,
        _2512,
        _2513,
        _2515,
        _2517,
        _2519,
        _2521,
        _2523,
    )
    from mastapy._private.system_model.part_model import _2639, _2640

    Self = TypeVar("Self", bound="Socket")
    CastSelf = TypeVar("CastSelf", bound="Socket._Cast_Socket")


__docformat__ = "restructuredtext en"
__all__ = ("Socket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Socket:
    """Special nested class for casting Socket to subclasses."""

    __parent__: "Socket"

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2457.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2457

        return self.__parent__._cast(_2457.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2458.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2458

        return self.__parent__._cast(_2458.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2465.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2465

        return self.__parent__._cast(_2465.CVTPulleySocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2467.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2467

        return self.__parent__._cast(_2467.CylindricalSocket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "_2469.ElectricMachineStatorSocket":
        from mastapy._private.system_model.connections_and_sockets import _2469

        return self.__parent__._cast(_2469.ElectricMachineStatorSocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2470.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2470

        return self.__parent__._cast(_2470.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2471.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2471

        return self.__parent__._cast(_2471.InnerShaftSocketBase)

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
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2475.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2475

        return self.__parent__._cast(_2475.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2476.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2476

        return self.__parent__._cast(_2476.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2477.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2477

        return self.__parent__._cast(_2477.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2479.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2479

        return self.__parent__._cast(_2479.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2480.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2480

        return self.__parent__._cast(_2480.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2481.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2481

        return self.__parent__._cast(_2481.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2484.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2484

        return self.__parent__._cast(_2484.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2485.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2485

        return self.__parent__._cast(_2485.ShaftSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2491.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2491

        return self.__parent__._cast(_2491.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2493.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2493

        return self.__parent__._cast(_2493.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2495.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2495

        return self.__parent__._cast(_2495.BevelGearTeethSocket)

    @property
    def concept_gear_teeth_socket(self: "CastSelf") -> "_2497.ConceptGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2497

        return self.__parent__._cast(_2497.ConceptGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2499.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2499

        return self.__parent__._cast(_2499.ConicalGearTeethSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2501.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2501

        return self.__parent__._cast(_2501.CylindricalGearTeethSocket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "_2503.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2503

        return self.__parent__._cast(_2503.FaceGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2505.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2505

        return self.__parent__._cast(_2505.GearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2507.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2507

        return self.__parent__._cast(_2507.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2508.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2508

        return self.__parent__._cast(_2508.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2512.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2512

        return self.__parent__._cast(_2512.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2513.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2513

        return self.__parent__._cast(_2513.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2515.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2515

        return self.__parent__._cast(_2515.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2517.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2517

        return self.__parent__._cast(_2517.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2519.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2519

        return self.__parent__._cast(_2519.StraightBevelGearTeethSocket)

    @property
    def worm_gear_teeth_socket(self: "CastSelf") -> "_2521.WormGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2521

        return self.__parent__._cast(_2521.WormGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2523.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2523

        return self.__parent__._cast(_2523.ZerolBevelGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2524.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2524,
        )

        return self.__parent__._cast(_2524.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2525.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2525,
        )

        return self.__parent__._cast(_2525.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2527.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2527,
        )

        return self.__parent__._cast(_2527.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2528.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2528,
        )

        return self.__parent__._cast(_2528.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2530.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2530,
        )

        return self.__parent__._cast(_2530.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2531.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2531,
        )

        return self.__parent__._cast(_2531.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2534.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2534,
        )

        return self.__parent__._cast(_2534.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2536.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2536,
        )

        return self.__parent__._cast(_2536.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2538.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2538,
        )

        return self.__parent__._cast(_2538.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2540.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2540,
        )

        return self.__parent__._cast(_2540.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2542.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2542,
        )

        return self.__parent__._cast(_2542.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2544.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2544,
        )

        return self.__parent__._cast(_2544.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2545.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2545,
        )

        return self.__parent__._cast(_2545.TorqueConverterTurbineSocket)

    @property
    def socket(self: "CastSelf") -> "Socket":
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
class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def connected_components(self: "Self") -> "List[_2639.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connections(self: "Self") -> "List[_2463.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def owner(self: "Self") -> "_2639.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Owner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "_2639.Component"
    ) -> "_2640.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
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
    def connect_to_socket(
        self: "Self", socket: "Socket"
    ) -> "_2640.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connection_to(self: "Self", socket: "Socket") -> "_2463.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "ConnectionTo", socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_possible_sockets_to_connect_to(
        self: "Self", component_to_connect_to: "_2639.Component"
    ) -> "List[Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetPossibleSocketsToConnectTo",
                component_to_connect_to.wrapped if component_to_connect_to else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Socket":
        """Cast to another type.

        Returns:
            _Cast_Socket
        """
        return _Cast_Socket(self)
