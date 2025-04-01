"""InterMountableComponentConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2463

_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.connections_and_sockets import (
        _2459,
        _2464,
        _2483,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2533,
        _2535,
        _2537,
        _2539,
        _2541,
        _2543,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2532
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

    Self = TypeVar("Self", bound="InterMountableComponentConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnection._Cast_InterMountableComponentConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnection:
    """Special nested class for casting InterMountableComponentConnection to subclasses."""

    __parent__: "InterMountableComponentConnection"

    @property
    def connection(self: "CastSelf") -> "_2463.Connection":
        return self.__parent__._cast(_2463.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def belt_connection(self: "CastSelf") -> "_2459.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2459

        return self.__parent__._cast(_2459.BeltConnection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2464.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2464

        return self.__parent__._cast(_2464.CVTBeltConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2483.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2483

        return self.__parent__._cast(_2483.RollingRingConnection)

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
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "InterMountableComponentConnection":
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
class InterMountableComponentConnection(_2463.Connection):
    """InterMountableComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_modal_damping_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return temp

    @additional_modal_damping_ratio.setter
    @enforce_parameter_types
    def additional_modal_damping_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalModalDampingRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_InterMountableComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnection
        """
        return _Cast_InterMountableComponentConnection(self)
