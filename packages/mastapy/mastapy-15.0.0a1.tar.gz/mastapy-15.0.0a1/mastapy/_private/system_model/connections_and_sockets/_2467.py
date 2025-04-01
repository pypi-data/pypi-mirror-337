"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2487

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2457,
        _2458,
        _2465,
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
    from mastapy._private.system_model.connections_and_sockets.gears import _2501

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2487.Socket":
        return self.__parent__._cast(_2487.Socket)

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
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2501.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2501

        return self.__parent__._cast(_2501.CylindricalGearTeethSocket)

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
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2487.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
