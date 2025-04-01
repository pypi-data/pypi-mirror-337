"""DesignEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2391
    from mastapy._private.system_model.connections_and_sockets import (
        _2456,
        _2459,
        _2460,
        _2463,
        _2464,
        _2472,
        _2478,
        _2483,
        _2486,
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
    from mastapy._private.system_model.part_model import (
        _2628,
        _2629,
        _2630,
        _2631,
        _2634,
        _2637,
        _2638,
        _2639,
        _2642,
        _2643,
        _2648,
        _2649,
        _2650,
        _2651,
        _2658,
        _2659,
        _2660,
        _2661,
        _2662,
        _2664,
        _2666,
        _2668,
        _2670,
        _2671,
        _2674,
        _2676,
        _2677,
        _2679,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2780,
        _2782,
        _2783,
        _2785,
        _2786,
        _2788,
        _2789,
        _2791,
        _2792,
        _2793,
        _2794,
        _2796,
        _2803,
        _2804,
        _2805,
        _2811,
        _2812,
        _2813,
        _2815,
        _2816,
        _2817,
        _2818,
        _2819,
        _2821,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2771, _2772, _2773
    from mastapy._private.system_model.part_model.gears import (
        _2715,
        _2716,
        _2717,
        _2718,
        _2719,
        _2720,
        _2721,
        _2722,
        _2723,
        _2724,
        _2725,
        _2726,
        _2727,
        _2728,
        _2729,
        _2730,
        _2731,
        _2732,
        _2734,
        _2736,
        _2737,
        _2738,
        _2739,
        _2740,
        _2741,
        _2742,
        _2743,
        _2744,
        _2746,
        _2747,
        _2748,
        _2749,
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
        _2755,
        _2756,
        _2757,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2682
    from mastapy._private.utility.model_validation import _1971, _1972
    from mastapy._private.utility.scripting import _1919

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

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
    def connection(self: "CastSelf") -> "_2463.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2463

        return self.__parent__._cast(_2463.Connection)

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
    def assembly(self: "CastSelf") -> "_2628.Assembly":
        from mastapy._private.system_model.part_model import _2628

        return self.__parent__._cast(_2628.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2629.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2629

        return self.__parent__._cast(_2629.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2630.AbstractShaft":
        from mastapy._private.system_model.part_model import _2630

        return self.__parent__._cast(_2630.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2631.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2631

        return self.__parent__._cast(_2631.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2634.Bearing":
        from mastapy._private.system_model.part_model import _2634

        return self.__parent__._cast(_2634.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2637.Bolt":
        from mastapy._private.system_model.part_model import _2637

        return self.__parent__._cast(_2637.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2638.BoltedJoint":
        from mastapy._private.system_model.part_model import _2638

        return self.__parent__._cast(_2638.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        from mastapy._private.system_model.part_model import _2639

        return self.__parent__._cast(_2639.Component)

    @property
    def connector(self: "CastSelf") -> "_2642.Connector":
        from mastapy._private.system_model.part_model import _2642

        return self.__parent__._cast(_2642.Connector)

    @property
    def datum(self: "CastSelf") -> "_2643.Datum":
        from mastapy._private.system_model.part_model import _2643

        return self.__parent__._cast(_2643.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2648.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2648

        return self.__parent__._cast(_2648.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2649.FEPart":
        from mastapy._private.system_model.part_model import _2649

        return self.__parent__._cast(_2649.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2650.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2650

        return self.__parent__._cast(_2650.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2651.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2651

        return self.__parent__._cast(_2651.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2658.MassDisc":
        from mastapy._private.system_model.part_model import _2658

        return self.__parent__._cast(_2658.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2659.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2660.Microphone":
        from mastapy._private.system_model.part_model import _2660

        return self.__parent__._cast(_2660.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2661.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2661

        return self.__parent__._cast(_2661.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
        from mastapy._private.system_model.part_model import _2662

        return self.__parent__._cast(_2662.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2664.OilSeal":
        from mastapy._private.system_model.part_model import _2664

        return self.__parent__._cast(_2664.OilSeal)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

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
    def root_assembly(self: "CastSelf") -> "_2674.RootAssembly":
        from mastapy._private.system_model.part_model import _2674

        return self.__parent__._cast(_2674.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2676.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2676

        return self.__parent__._cast(_2676.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2677.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2677

        return self.__parent__._cast(_2677.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2679.VirtualComponent":
        from mastapy._private.system_model.part_model import _2679

        return self.__parent__._cast(_2679.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2682.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2682

        return self.__parent__._cast(_2682.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2715.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2715

        return self.__parent__._cast(_2715.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2716.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2716

        return self.__parent__._cast(_2716.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2717.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2717

        return self.__parent__._cast(_2717.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2718.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2718

        return self.__parent__._cast(_2718.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "_2722.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2722

        return self.__parent__._cast(_2722.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2723.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2723

        return self.__parent__._cast(_2723.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2724.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2724

        return self.__parent__._cast(_2724.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2725.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2725

        return self.__parent__._cast(_2725.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2726.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2726

        return self.__parent__._cast(_2726.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2727.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2727

        return self.__parent__._cast(_2727.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2728.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2728

        return self.__parent__._cast(_2728.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2729.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2729

        return self.__parent__._cast(_2729.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2730.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2730

        return self.__parent__._cast(_2730.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2731.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2731

        return self.__parent__._cast(_2731.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2732.Gear":
        from mastapy._private.system_model.part_model.gears import _2732

        return self.__parent__._cast(_2732.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2734.GearSet":
        from mastapy._private.system_model.part_model.gears import _2734

        return self.__parent__._cast(_2734.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2736.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2736

        return self.__parent__._cast(_2736.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2737.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2737

        return self.__parent__._cast(_2737.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2738.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2738

        return self.__parent__._cast(_2738.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2739.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2739

        return self.__parent__._cast(_2739.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2740.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2740

        return self.__parent__._cast(_2740.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2741.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2741

        return self.__parent__._cast(_2741.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2742.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2742

        return self.__parent__._cast(_2742.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2743.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2743

        return self.__parent__._cast(_2743.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2744.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2744

        return self.__parent__._cast(_2744.PlanetaryGearSet)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2746.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2746

        return self.__parent__._cast(_2746.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2747.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2747

        return self.__parent__._cast(_2747.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2748.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2748

        return self.__parent__._cast(_2748.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2749.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2749

        return self.__parent__._cast(_2749.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2750.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2751.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.StraightBevelGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2755.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2756.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2757.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2771.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2771

        return self.__parent__._cast(_2771.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2772.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2772

        return self.__parent__._cast(_2772.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2773.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2773

        return self.__parent__._cast(_2773.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2780.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2780

        return self.__parent__._cast(_2780.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2782.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2782

        return self.__parent__._cast(_2782.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2783.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2783

        return self.__parent__._cast(_2783.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2785.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2785

        return self.__parent__._cast(_2785.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2786.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2786

        return self.__parent__._cast(_2786.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2788.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2788

        return self.__parent__._cast(_2788.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2789.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2789

        return self.__parent__._cast(_2789.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2791.CVT":
        from mastapy._private.system_model.part_model.couplings import _2791

        return self.__parent__._cast(_2791.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2792.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2792

        return self.__parent__._cast(_2792.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2793.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2793

        return self.__parent__._cast(_2793.PartToPartShearCoupling)

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
    def rolling_ring_assembly(self: "CastSelf") -> "_2804.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2804

        return self.__parent__._cast(_2804.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2805.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2805

        return self.__parent__._cast(_2805.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2811.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2811

        return self.__parent__._cast(_2811.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2812.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2812

        return self.__parent__._cast(_2812.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2813.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2813

        return self.__parent__._cast(_2813.Synchroniser)

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
    def torque_converter(self: "CastSelf") -> "_2818.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2819.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2819

        return self.__parent__._cast(_2819.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2821.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.TorqueConverterTurbine)

    @property
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

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
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

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
    def design_properties(self: "Self") -> "_2391.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_status_errors(self: "Self") -> "List[_1972.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1971.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def user_specified_data(self: "Self") -> "_1919.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
