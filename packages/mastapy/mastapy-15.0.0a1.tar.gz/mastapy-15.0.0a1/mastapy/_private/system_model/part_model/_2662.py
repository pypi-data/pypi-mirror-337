"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2639

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.connections_and_sockets import (
        _2460,
        _2463,
        _2467,
    )
    from mastapy._private.system_model.part_model import (
        _2630,
        _2634,
        _2640,
        _2642,
        _2658,
        _2659,
        _2664,
        _2666,
        _2668,
        _2670,
        _2671,
        _2677,
        _2679,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2783,
        _2786,
        _2789,
        _2792,
        _2794,
        _2796,
        _2803,
        _2805,
        _2812,
        _2815,
        _2816,
        _2817,
        _2819,
        _2821,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2773
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2717,
        _2719,
        _2720,
        _2721,
        _2723,
        _2725,
        _2727,
        _2729,
        _2730,
        _2732,
        _2736,
        _2738,
        _2740,
        _2742,
        _2746,
        _2748,
        _2750,
        _2752,
        _2753,
        _2754,
        _2756,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        return self.__parent__._cast(_2639.Component)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2634.Bearing":
        from mastapy._private.system_model.part_model import _2634

        return self.__parent__._cast(_2634.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2642.Connector":
        from mastapy._private.system_model.part_model import _2642

        return self.__parent__._cast(_2642.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2658.MassDisc":
        from mastapy._private.system_model.part_model import _2658

        return self.__parent__._cast(_2658.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2659.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2664.OilSeal":
        from mastapy._private.system_model.part_model import _2664

        return self.__parent__._cast(_2664.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2668.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2668

        return self.__parent__._cast(_2668.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2670.PointLoad":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2671.PowerLoad":
        from mastapy._private.system_model.part_model import _2671

        return self.__parent__._cast(_2671.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2677.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2677

        return self.__parent__._cast(_2677.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2679.VirtualComponent":
        from mastapy._private.system_model.part_model import _2679

        return self.__parent__._cast(_2679.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2715.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2715

        return self.__parent__._cast(_2715.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2717.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2717

        return self.__parent__._cast(_2717.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2719.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2719

        return self.__parent__._cast(_2719.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2720.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2720

        return self.__parent__._cast(_2720.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2721.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2721

        return self.__parent__._cast(_2721.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2723.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2723

        return self.__parent__._cast(_2723.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2725.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2725

        return self.__parent__._cast(_2725.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2727.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2727

        return self.__parent__._cast(_2727.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2729.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2729

        return self.__parent__._cast(_2729.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2730.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2730

        return self.__parent__._cast(_2730.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2732.Gear":
        from mastapy._private.system_model.part_model.gears import _2732

        return self.__parent__._cast(_2732.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2736.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2736

        return self.__parent__._cast(_2736.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2738.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2738

        return self.__parent__._cast(_2738.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2740.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2740

        return self.__parent__._cast(_2740.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2742.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2742

        return self.__parent__._cast(_2742.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2746.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2746

        return self.__parent__._cast(_2746.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2748.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2748

        return self.__parent__._cast(_2748.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2750.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2752.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2753.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2753

        return self.__parent__._cast(_2753.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2754.WormGear":
        from mastapy._private.system_model.part_model.gears import _2754

        return self.__parent__._cast(_2754.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2756.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2773.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2773

        return self.__parent__._cast(_2773.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2783.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2783

        return self.__parent__._cast(_2783.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2786.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2786

        return self.__parent__._cast(_2786.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2789.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2789

        return self.__parent__._cast(_2789.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2792.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2792

        return self.__parent__._cast(_2792.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2794.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2794

        return self.__parent__._cast(_2794.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2796.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2796

        return self.__parent__._cast(_2796.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2803.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2803

        return self.__parent__._cast(_2803.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2805.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2805

        return self.__parent__._cast(_2805.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2812.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2812

        return self.__parent__._cast(_2812.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2815.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2815

        return self.__parent__._cast(_2815.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2816.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2816

        return self.__parent__._cast(_2816.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2817.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2817

        return self.__parent__._cast(_2817.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2819.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2819

        return self.__parent__._cast(_2819.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2821.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2639.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2630.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2463.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2467.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2630.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2460.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2630.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2640.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
