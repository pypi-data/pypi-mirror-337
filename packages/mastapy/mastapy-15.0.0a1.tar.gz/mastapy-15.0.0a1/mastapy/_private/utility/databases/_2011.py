"""NamedDatabaseItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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

_NAMED_DATABASE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NamedDatabaseItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _2067
    from mastapy._private.bearings.bearing_results.rolling import _2162
    from mastapy._private.bolts import _1642, _1644, _1646
    from mastapy._private.cycloidal import _1632, _1639
    from mastapy._private.detailed_rigid_connectors.splines import _1592
    from mastapy._private.electric_machines import _1397, _1411, _1430, _1445
    from mastapy._private.gears import _425
    from mastapy._private.gears.gear_designs import _1038, _1040, _1043
    from mastapy._private.gears.gear_designs.cylindrical import _1117, _1125
    from mastapy._private.gears.manufacturing.bevel import _895
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _802,
        _803,
        _804,
        _805,
        _806,
        _808,
        _809,
        _810,
        _811,
        _814,
    )
    from mastapy._private.gears.materials import (
        _667,
        _670,
        _672,
        _677,
        _681,
        _689,
        _691,
        _694,
        _698,
        _701,
    )
    from mastapy._private.gears.rating.cylindrical import _538, _554
    from mastapy._private.materials import _326, _336, _350, _352, _356
    from mastapy._private.math_utility.optimisation import _1723
    from mastapy._private.nodal_analysis import _53
    from mastapy._private.shafts import _24, _43, _46
    from mastapy._private.system_model.optimization import _2417, _2420, _2425, _2426
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2766,
    )
    from mastapy._private.utility import _1757
    from mastapy._private.utility.databases import _2012

    Self = TypeVar("Self", bound="NamedDatabaseItem")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabaseItem._Cast_NamedDatabaseItem")


__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabaseItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabaseItem:
    """Special nested class for casting NamedDatabaseItem to subclasses."""

    __parent__: "NamedDatabaseItem"

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def shaft_settings_item(self: "CastSelf") -> "_43.ShaftSettingsItem":
        from mastapy._private.shafts import _43

        return self.__parent__._cast(_43.ShaftSettingsItem)

    @property
    def simple_shaft_definition(self: "CastSelf") -> "_46.SimpleShaftDefinition":
        from mastapy._private.shafts import _46

        return self.__parent__._cast(_46.SimpleShaftDefinition)

    @property
    def analysis_settings_item(self: "CastSelf") -> "_53.AnalysisSettingsItem":
        from mastapy._private.nodal_analysis import _53

        return self.__parent__._cast(_53.AnalysisSettingsItem)

    @property
    def bearing_material(self: "CastSelf") -> "_326.BearingMaterial":
        from mastapy._private.materials import _326

        return self.__parent__._cast(_326.BearingMaterial)

    @property
    def fluid(self: "CastSelf") -> "_336.Fluid":
        from mastapy._private.materials import _336

        return self.__parent__._cast(_336.Fluid)

    @property
    def lubrication_detail(self: "CastSelf") -> "_350.LubricationDetail":
        from mastapy._private.materials import _350

        return self.__parent__._cast(_350.LubricationDetail)

    @property
    def material(self: "CastSelf") -> "_352.Material":
        from mastapy._private.materials import _352

        return self.__parent__._cast(_352.Material)

    @property
    def materials_settings_item(self: "CastSelf") -> "_356.MaterialsSettingsItem":
        from mastapy._private.materials import _356

        return self.__parent__._cast(_356.MaterialsSettingsItem)

    @property
    def pocketing_power_loss_coefficients(
        self: "CastSelf",
    ) -> "_425.PocketingPowerLossCoefficients":
        from mastapy._private.gears import _425

        return self.__parent__._cast(_425.PocketingPowerLossCoefficients)

    @property
    def cylindrical_gear_design_and_rating_settings_item(
        self: "CastSelf",
    ) -> "_538.CylindricalGearDesignAndRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _538

        return self.__parent__._cast(_538.CylindricalGearDesignAndRatingSettingsItem)

    @property
    def cylindrical_plastic_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_554.CylindricalPlasticGearRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _554

        return self.__parent__._cast(_554.CylindricalPlasticGearRatingSettingsItem)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_667.AGMACylindricalGearMaterial":
        from mastapy._private.gears.materials import _667

        return self.__parent__._cast(_667.AGMACylindricalGearMaterial)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_670.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _670

        return self.__parent__._cast(_670.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "_672.BevelGearMaterial":
        from mastapy._private.gears.materials import _672

        return self.__parent__._cast(_672.BevelGearMaterial)

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_677.CylindricalGearMaterial":
        from mastapy._private.gears.materials import _677

        return self.__parent__._cast(_677.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_681.GearMaterial":
        from mastapy._private.gears.materials import _681

        return self.__parent__._cast(_681.GearMaterial)

    @property
    def iso_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_689.ISOCylindricalGearMaterial":
        from mastapy._private.gears.materials import _689

        return self.__parent__._cast(_689.ISOCylindricalGearMaterial)

    @property
    def isotr1417912001_coefficient_of_friction_constants(
        self: "CastSelf",
    ) -> "_691.ISOTR1417912001CoefficientOfFrictionConstants":
        from mastapy._private.gears.materials import _691

        return self.__parent__._cast(_691.ISOTR1417912001CoefficientOfFrictionConstants)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_material(
        self: "CastSelf",
    ) -> "_694.KlingelnbergCycloPalloidConicalGearMaterial":
        from mastapy._private.gears.materials import _694

        return self.__parent__._cast(_694.KlingelnbergCycloPalloidConicalGearMaterial)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_698.PlasticCylindricalGearMaterial":
        from mastapy._private.gears.materials import _698

        return self.__parent__._cast(_698.PlasticCylindricalGearMaterial)

    @property
    def raw_material(self: "CastSelf") -> "_701.RawMaterial":
        from mastapy._private.gears.materials import _701

        return self.__parent__._cast(_701.RawMaterial)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_802.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _802

        return self.__parent__._cast(_802.CylindricalGearAbstractCutterDesign)

    @property
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "_803.CylindricalGearFormGrindingWheel":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _803

        return self.__parent__._cast(_803.CylindricalGearFormGrindingWheel)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "_804.CylindricalGearGrindingWorm":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _804

        return self.__parent__._cast(_804.CylindricalGearGrindingWorm)

    @property
    def cylindrical_gear_hob_design(
        self: "CastSelf",
    ) -> "_805.CylindricalGearHobDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _805

        return self.__parent__._cast(_805.CylindricalGearHobDesign)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "_806.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _806

        return self.__parent__._cast(_806.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_808.CylindricalGearRackDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _808

        return self.__parent__._cast(_808.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

        return self.__parent__._cast(_809.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_810.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _810

        return self.__parent__._cast(_810.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_811.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _811

        return self.__parent__._cast(_811.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_814.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _814

        return self.__parent__._cast(_814.InvoluteCutterDesign)

    @property
    def manufacturing_machine(self: "CastSelf") -> "_895.ManufacturingMachine":
        from mastapy._private.gears.manufacturing.bevel import _895

        return self.__parent__._cast(_895.ManufacturingMachine)

    @property
    def bevel_hypoid_gear_design_settings_item(
        self: "CastSelf",
    ) -> "_1038.BevelHypoidGearDesignSettingsItem":
        from mastapy._private.gears.gear_designs import _1038

        return self.__parent__._cast(_1038.BevelHypoidGearDesignSettingsItem)

    @property
    def bevel_hypoid_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_1040.BevelHypoidGearRatingSettingsItem":
        from mastapy._private.gears.gear_designs import _1040

        return self.__parent__._cast(_1040.BevelHypoidGearRatingSettingsItem)

    @property
    def design_constraints_collection(
        self: "CastSelf",
    ) -> "_1043.DesignConstraintsCollection":
        from mastapy._private.gears.gear_designs import _1043

        return self.__parent__._cast(_1043.DesignConstraintsCollection)

    @property
    def cylindrical_gear_design_constraints(
        self: "CastSelf",
    ) -> "_1117.CylindricalGearDesignConstraints":
        from mastapy._private.gears.gear_designs.cylindrical import _1117

        return self.__parent__._cast(_1117.CylindricalGearDesignConstraints)

    @property
    def cylindrical_gear_micro_geometry_settings_item(
        self: "CastSelf",
    ) -> "_1125.CylindricalGearMicroGeometrySettingsItem":
        from mastapy._private.gears.gear_designs.cylindrical import _1125

        return self.__parent__._cast(_1125.CylindricalGearMicroGeometrySettingsItem)

    @property
    def general_electric_machine_material(
        self: "CastSelf",
    ) -> "_1397.GeneralElectricMachineMaterial":
        from mastapy._private.electric_machines import _1397

        return self.__parent__._cast(_1397.GeneralElectricMachineMaterial)

    @property
    def magnet_material(self: "CastSelf") -> "_1411.MagnetMaterial":
        from mastapy._private.electric_machines import _1411

        return self.__parent__._cast(_1411.MagnetMaterial)

    @property
    def stator_rotor_material(self: "CastSelf") -> "_1430.StatorRotorMaterial":
        from mastapy._private.electric_machines import _1430

        return self.__parent__._cast(_1430.StatorRotorMaterial)

    @property
    def winding_material(self: "CastSelf") -> "_1445.WindingMaterial":
        from mastapy._private.electric_machines import _1445

        return self.__parent__._cast(_1445.WindingMaterial)

    @property
    def spline_material(self: "CastSelf") -> "_1592.SplineMaterial":
        from mastapy._private.detailed_rigid_connectors.splines import _1592

        return self.__parent__._cast(_1592.SplineMaterial)

    @property
    def cycloidal_disc_material(self: "CastSelf") -> "_1632.CycloidalDiscMaterial":
        from mastapy._private.cycloidal import _1632

        return self.__parent__._cast(_1632.CycloidalDiscMaterial)

    @property
    def ring_pins_material(self: "CastSelf") -> "_1639.RingPinsMaterial":
        from mastapy._private.cycloidal import _1639

        return self.__parent__._cast(_1639.RingPinsMaterial)

    @property
    def bolted_joint_material(self: "CastSelf") -> "_1642.BoltedJointMaterial":
        from mastapy._private.bolts import _1642

        return self.__parent__._cast(_1642.BoltedJointMaterial)

    @property
    def bolt_geometry(self: "CastSelf") -> "_1644.BoltGeometry":
        from mastapy._private.bolts import _1644

        return self.__parent__._cast(_1644.BoltGeometry)

    @property
    def bolt_material(self: "CastSelf") -> "_1646.BoltMaterial":
        from mastapy._private.bolts import _1646

        return self.__parent__._cast(_1646.BoltMaterial)

    @property
    def pareto_optimisation_strategy(
        self: "CastSelf",
    ) -> "_1723.ParetoOptimisationStrategy":
        from mastapy._private.math_utility.optimisation import _1723

        return self.__parent__._cast(_1723.ParetoOptimisationStrategy)

    @property
    def bearing_settings_item(self: "CastSelf") -> "_2067.BearingSettingsItem":
        from mastapy._private.bearings import _2067

        return self.__parent__._cast(_2067.BearingSettingsItem)

    @property
    def iso14179_settings(self: "CastSelf") -> "_2162.ISO14179Settings":
        from mastapy._private.bearings.bearing_results.rolling import _2162

        return self.__parent__._cast(_2162.ISO14179Settings)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2417.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2417

        return self.__parent__._cast(_2417.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2420.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2420

        return self.__parent__._cast(_2420.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "_2425.OptimizationStrategy":
        from mastapy._private.system_model.optimization import _2425

        return self.__parent__._cast(_2425.OptimizationStrategy)

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2426.OptimizationStrategyBase":
        from mastapy._private.system_model.optimization import _2426

        return self.__parent__._cast(_2426.OptimizationStrategyBase)

    @property
    def supercharger_rotor_set(self: "CastSelf") -> "_2766.SuperchargerRotorSet":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2766,
        )

        return self.__parent__._cast(_2766.SuperchargerRotorSet)

    @property
    def named_database_item(self: "CastSelf") -> "NamedDatabaseItem":
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
class NamedDatabaseItem(_0.APIBase):
    """NamedDatabaseItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE_ITEM

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
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    def history(self: "Self") -> "_1757.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def database_key(self: "Self") -> "_2012.NamedKey":
        """mastapy.utility.databases.NamedKey"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseKey")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @database_key.setter
    @enforce_parameter_types
    def database_key(self: "Self", value: "_2012.NamedKey") -> None:
        pythonnet_property_set(self.wrapped, "DatabaseKey", value.wrapped)

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
    def cast_to(self: "Self") -> "_Cast_NamedDatabaseItem":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabaseItem
        """
        return _Cast_NamedDatabaseItem(self)
