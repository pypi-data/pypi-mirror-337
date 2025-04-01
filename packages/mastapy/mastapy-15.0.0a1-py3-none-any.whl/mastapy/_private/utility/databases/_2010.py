"""NamedDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2012, _2014

_NAMED_DATABASE = python_net_import("SMT.MastaAPI.Utility.Databases", "NamedDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings import _2066
    from mastapy._private.bearings.bearing_results.rolling import _2163
    from mastapy._private.bolts import _1643, _1645, _1647, _1652
    from mastapy._private.cycloidal import _1633, _1640
    from mastapy._private.electric_machines import _1398, _1412, _1431, _1446
    from mastapy._private.gears import _426
    from mastapy._private.gears.gear_designs import _1037, _1039, _1042
    from mastapy._private.gears.gear_designs.cylindrical import _1118, _1124
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1015,
        _1017,
        _1018,
        _1020,
        _1021,
        _1022,
        _1023,
        _1024,
        _1025,
        _1026,
        _1027,
        _1028,
        _1030,
        _1031,
        _1032,
        _1033,
    )
    from mastapy._private.gears.manufacturing.bevel import _896
    from mastapy._private.gears.manufacturing.cylindrical import _706, _711, _722
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _801,
        _807,
        _812,
        _813,
    )
    from mastapy._private.gears.materials import (
        _669,
        _671,
        _673,
        _675,
        _676,
        _678,
        _679,
        _682,
        _692,
        _693,
        _702,
    )
    from mastapy._private.gears.rating.cylindrical import _537, _553
    from mastapy._private.materials import _327, _330, _337, _351, _353, _355
    from mastapy._private.math_utility.optimisation import _1714, _1726
    from mastapy._private.nodal_analysis import _52
    from mastapy._private.shafts import _25, _42
    from mastapy._private.system_model.optimization import _2419, _2427
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2767,
    )
    from mastapy._private.utility.databases import _2006, _2011

    Self = TypeVar("Self", bound="NamedDatabase")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabase._Cast_NamedDatabase")

TValue = TypeVar("TValue", bound="_2011.NamedDatabaseItem")

__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabase:
    """Special nested class for casting NamedDatabase to subclasses."""

    __parent__: "NamedDatabase"

    @property
    def sql_database(self: "CastSelf") -> "_2014.SQLDatabase":
        return self.__parent__._cast(_2014.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2006.Database":
        from mastapy._private.utility.databases import _2006

        return self.__parent__._cast(_2006.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def shaft_settings_database(self: "CastSelf") -> "_42.ShaftSettingsDatabase":
        from mastapy._private.shafts import _42

        return self.__parent__._cast(_42.ShaftSettingsDatabase)

    @property
    def analysis_settings_database(self: "CastSelf") -> "_52.AnalysisSettingsDatabase":
        from mastapy._private.nodal_analysis import _52

        return self.__parent__._cast(_52.AnalysisSettingsDatabase)

    @property
    def bearing_material_database(self: "CastSelf") -> "_327.BearingMaterialDatabase":
        from mastapy._private.materials import _327

        return self.__parent__._cast(_327.BearingMaterialDatabase)

    @property
    def component_material_database(
        self: "CastSelf",
    ) -> "_330.ComponentMaterialDatabase":
        from mastapy._private.materials import _330

        return self.__parent__._cast(_330.ComponentMaterialDatabase)

    @property
    def fluid_database(self: "CastSelf") -> "_337.FluidDatabase":
        from mastapy._private.materials import _337

        return self.__parent__._cast(_337.FluidDatabase)

    @property
    def lubrication_detail_database(
        self: "CastSelf",
    ) -> "_351.LubricationDetailDatabase":
        from mastapy._private.materials import _351

        return self.__parent__._cast(_351.LubricationDetailDatabase)

    @property
    def material_database(self: "CastSelf") -> "_353.MaterialDatabase":
        from mastapy._private.materials import _353

        return self.__parent__._cast(_353.MaterialDatabase)

    @property
    def materials_settings_database(
        self: "CastSelf",
    ) -> "_355.MaterialsSettingsDatabase":
        from mastapy._private.materials import _355

        return self.__parent__._cast(_355.MaterialsSettingsDatabase)

    @property
    def pocketing_power_loss_coefficients_database(
        self: "CastSelf",
    ) -> "_426.PocketingPowerLossCoefficientsDatabase":
        from mastapy._private.gears import _426

        return self.__parent__._cast(_426.PocketingPowerLossCoefficientsDatabase)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "CastSelf",
    ) -> "_537.CylindricalGearDesignAndRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _537

        return self.__parent__._cast(
            _537.CylindricalGearDesignAndRatingSettingsDatabase
        )

    @property
    def cylindrical_plastic_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_553.CylindricalPlasticGearRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _553

        return self.__parent__._cast(_553.CylindricalPlasticGearRatingSettingsDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_669.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _669

        return self.__parent__._cast(_669.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_671.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _671

        return self.__parent__._cast(_671.BevelGearISOMaterialDatabase)

    @property
    def bevel_gear_material_database(
        self: "CastSelf",
    ) -> "_673.BevelGearMaterialDatabase":
        from mastapy._private.gears.materials import _673

        return self.__parent__._cast(_673.BevelGearMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_675.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _675

        return self.__parent__._cast(_675.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_676.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _676

        return self.__parent__._cast(_676.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_678.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _678

        return self.__parent__._cast(_678.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_679.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _679

        return self.__parent__._cast(_679.CylindricalGearPlasticMaterialDatabase)

    @property
    def gear_material_database(self: "CastSelf") -> "_682.GearMaterialDatabase":
        from mastapy._private.gears.materials import _682

        return self.__parent__._cast(_682.GearMaterialDatabase)

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "CastSelf",
    ) -> "_692.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        from mastapy._private.gears.materials import _692

        return self.__parent__._cast(
            _692.ISOTR1417912001CoefficientOfFrictionConstantsDatabase
        )

    @property
    def klingelnberg_conical_gear_material_database(
        self: "CastSelf",
    ) -> "_693.KlingelnbergConicalGearMaterialDatabase":
        from mastapy._private.gears.materials import _693

        return self.__parent__._cast(_693.KlingelnbergConicalGearMaterialDatabase)

    @property
    def raw_material_database(self: "CastSelf") -> "_702.RawMaterialDatabase":
        from mastapy._private.gears.materials import _702

        return self.__parent__._cast(_702.RawMaterialDatabase)

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_706.CylindricalCutterDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _706

        return self.__parent__._cast(_706.CylindricalCutterDatabase)

    @property
    def cylindrical_hob_database(self: "CastSelf") -> "_711.CylindricalHobDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _711

        return self.__parent__._cast(_711.CylindricalHobDatabase)

    @property
    def cylindrical_shaper_database(
        self: "CastSelf",
    ) -> "_722.CylindricalShaperDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _722

        return self.__parent__._cast(_722.CylindricalShaperDatabase)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "CastSelf",
    ) -> "_801.CylindricalFormedWheelGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _801

        return self.__parent__._cast(_801.CylindricalFormedWheelGrinderDatabase)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "_807.CylindricalGearPlungeShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _807

        return self.__parent__._cast(_807.CylindricalGearPlungeShaverDatabase)

    @property
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "_812.CylindricalGearShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _812

        return self.__parent__._cast(_812.CylindricalGearShaverDatabase)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "_813.CylindricalWormGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _813

        return self.__parent__._cast(_813.CylindricalWormGrinderDatabase)

    @property
    def manufacturing_machine_database(
        self: "CastSelf",
    ) -> "_896.ManufacturingMachineDatabase":
        from mastapy._private.gears.manufacturing.bevel import _896

        return self.__parent__._cast(_896.ManufacturingMachineDatabase)

    @property
    def micro_geometry_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1015.MicroGeometryDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1015

        return self.__parent__._cast(
            _1015.MicroGeometryDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1017.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1017

        return self.__parent__._cast(
            _1017.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1018.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1018

        return self.__parent__._cast(
            _1018.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
        )

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1020.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1020

        return self.__parent__._cast(
            _1020.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1021.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1021

        return self.__parent__._cast(
            _1021.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1022.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1022

        return self.__parent__._cast(
            _1022.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1023.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1023

        return self.__parent__._cast(
            _1023.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1024.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1024

        return self.__parent__._cast(
            _1024.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1025.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1025

        return self.__parent__._cast(
            _1025.ParetoFaceGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1026.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1026

        return self.__parent__._cast(_1026.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1027.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1027

        return self.__parent__._cast(
            _1027.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1028.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1028

        return self.__parent__._cast(
            _1028.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1030.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1030

        return self.__parent__._cast(
            _1030.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1031.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1031

        return self.__parent__._cast(
            _1031.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1032.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1032

        return self.__parent__._cast(
            _1032.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1033.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1033

        return self.__parent__._cast(
            _1033.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def bevel_hypoid_gear_design_settings_database(
        self: "CastSelf",
    ) -> "_1037.BevelHypoidGearDesignSettingsDatabase":
        from mastapy._private.gears.gear_designs import _1037

        return self.__parent__._cast(_1037.BevelHypoidGearDesignSettingsDatabase)

    @property
    def bevel_hypoid_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_1039.BevelHypoidGearRatingSettingsDatabase":
        from mastapy._private.gears.gear_designs import _1039

        return self.__parent__._cast(_1039.BevelHypoidGearRatingSettingsDatabase)

    @property
    def design_constraint_collection_database(
        self: "CastSelf",
    ) -> "_1042.DesignConstraintCollectionDatabase":
        from mastapy._private.gears.gear_designs import _1042

        return self.__parent__._cast(_1042.DesignConstraintCollectionDatabase)

    @property
    def cylindrical_gear_design_constraints_database(
        self: "CastSelf",
    ) -> "_1118.CylindricalGearDesignConstraintsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1118

        return self.__parent__._cast(_1118.CylindricalGearDesignConstraintsDatabase)

    @property
    def cylindrical_gear_micro_geometry_settings_database(
        self: "CastSelf",
    ) -> "_1124.CylindricalGearMicroGeometrySettingsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1124

        return self.__parent__._cast(_1124.CylindricalGearMicroGeometrySettingsDatabase)

    @property
    def general_electric_machine_material_database(
        self: "CastSelf",
    ) -> "_1398.GeneralElectricMachineMaterialDatabase":
        from mastapy._private.electric_machines import _1398

        return self.__parent__._cast(_1398.GeneralElectricMachineMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1412.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1412

        return self.__parent__._cast(_1412.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1431.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1431

        return self.__parent__._cast(_1431.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1446.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1446

        return self.__parent__._cast(_1446.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1633.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1633

        return self.__parent__._cast(_1633.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1640.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1640

        return self.__parent__._cast(_1640.RingPinsMaterialDatabase)

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "_1643.BoltedJointMaterialDatabase":
        from mastapy._private.bolts import _1643

        return self.__parent__._cast(_1643.BoltedJointMaterialDatabase)

    @property
    def bolt_geometry_database(self: "CastSelf") -> "_1645.BoltGeometryDatabase":
        from mastapy._private.bolts import _1645

        return self.__parent__._cast(_1645.BoltGeometryDatabase)

    @property
    def bolt_material_database(self: "CastSelf") -> "_1647.BoltMaterialDatabase":
        from mastapy._private.bolts import _1647

        return self.__parent__._cast(_1647.BoltMaterialDatabase)

    @property
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "_1652.ClampedSectionMaterialDatabase":
        from mastapy._private.bolts import _1652

        return self.__parent__._cast(_1652.ClampedSectionMaterialDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1714.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1714

        return self.__parent__._cast(_1714.DesignSpaceSearchStrategyDatabase)

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1726.ParetoOptimisationStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1726

        return self.__parent__._cast(_1726.ParetoOptimisationStrategyDatabase)

    @property
    def bearing_settings_database(self: "CastSelf") -> "_2066.BearingSettingsDatabase":
        from mastapy._private.bearings import _2066

        return self.__parent__._cast(_2066.BearingSettingsDatabase)

    @property
    def iso14179_settings_database(
        self: "CastSelf",
    ) -> "_2163.ISO14179SettingsDatabase":
        from mastapy._private.bearings.bearing_results.rolling import _2163

        return self.__parent__._cast(_2163.ISO14179SettingsDatabase)

    @property
    def conical_gear_optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2419.ConicalGearOptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2419

        return self.__parent__._cast(_2419.ConicalGearOptimizationStrategyDatabase)

    @property
    def optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2427.OptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2427

        return self.__parent__._cast(_2427.OptimizationStrategyDatabase)

    @property
    def supercharger_rotor_set_database(
        self: "CastSelf",
    ) -> "_2767.SuperchargerRotorSetDatabase":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2767,
        )

        return self.__parent__._cast(_2767.SuperchargerRotorSetDatabase)

    @property
    def named_database(self: "CastSelf") -> "NamedDatabase":
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
class NamedDatabase(_2014.SQLDatabase[_2012.NamedKey, TValue]):
    """NamedDatabase

    This is a mastapy class.

    Generic Types:
        TValue
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def create(self: "Self", name: "str") -> "TValue":
        """TValue

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "Create", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def duplicate(
        self: "Self", new_name: "str", item: "_2011.NamedDatabaseItem"
    ) -> "_2011.NamedDatabaseItem":
        """mastapy.utility.databases.NamedDatabaseItem

        Args:
            new_name (str)
            item (mastapy.utility.databases.NamedDatabaseItem)
        """
        new_name = str(new_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Duplicate",
            new_name if new_name else "",
            item.wrapped if item else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_value(self: "Self", name: "str") -> "TValue":
        """TValue

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "GetValue", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def rename(
        self: "Self", item: "_2011.NamedDatabaseItem", new_name: "str"
    ) -> "bool":
        """bool

        Args:
            item (mastapy.utility.databases.NamedDatabaseItem)
            new_name (str)
        """
        new_name = str(new_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Rename",
            item.wrapped if item else None,
            new_name if new_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_NamedDatabase":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabase
        """
        return _Cast_NamedDatabase(self)
