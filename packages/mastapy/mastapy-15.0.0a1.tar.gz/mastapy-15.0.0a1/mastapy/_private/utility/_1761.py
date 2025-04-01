"""IndependentReportablePropertiesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.Utility", "IndependentReportablePropertiesBase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _2132
    from mastapy._private.bearings.bearing_results.rolling import _2164, _2260
    from mastapy._private.bearings.tolerances import _2104
    from mastapy._private.electric_machines import _1378
    from mastapy._private.electric_machines.load_cases_and_analyses import _1552
    from mastapy._private.gears import _429
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1123,
        _1154,
        _1162,
        _1163,
        _1166,
        _1167,
        _1176,
        _1184,
        _1186,
        _1190,
        _1194,
    )
    from mastapy._private.geometry import _392
    from mastapy._private.materials import _370
    from mastapy._private.materials.efficiency import _381
    from mastapy._private.math_utility.measured_data import _1740, _1741, _1742
    from mastapy._private.system_model.analyses_and_results.static_loads import _7637
    from mastapy._private.utility import _1774

    Self = TypeVar("Self", bound="IndependentReportablePropertiesBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
    )

T = TypeVar("T", bound="IndependentReportablePropertiesBase")

__docformat__ = "restructuredtext en"
__all__ = ("IndependentReportablePropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentReportablePropertiesBase:
    """Special nested class for casting IndependentReportablePropertiesBase to subclasses."""

    __parent__: "IndependentReportablePropertiesBase"

    @property
    def temperature_dependent_property(
        self: "CastSelf",
    ) -> "_370.TemperatureDependentProperty":
        from mastapy._private.materials import _370

        return self.__parent__._cast(_370.TemperatureDependentProperty)

    @property
    def oil_pump_detail(self: "CastSelf") -> "_381.OilPumpDetail":
        from mastapy._private.materials.efficiency import _381

        return self.__parent__._cast(_381.OilPumpDetail)

    @property
    def packaging_limits(self: "CastSelf") -> "_392.PackagingLimits":
        from mastapy._private.geometry import _392

        return self.__parent__._cast(_392.PackagingLimits)

    @property
    def specification_for_the_effect_of_oil_kinematic_viscosity(
        self: "CastSelf",
    ) -> "_429.SpecificationForTheEffectOfOilKinematicViscosity":
        from mastapy._private.gears import _429

        return self.__parent__._cast(
            _429.SpecificationForTheEffectOfOilKinematicViscosity
        )

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "CastSelf",
    ) -> "_1123.CylindricalGearMicroGeometrySettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1123

        return self.__parent__._cast(_1123.CylindricalGearMicroGeometrySettings)

    @property
    def hardened_material_properties(
        self: "CastSelf",
    ) -> "_1154.HardenedMaterialProperties":
        from mastapy._private.gears.gear_designs.cylindrical import _1154

        return self.__parent__._cast(_1154.HardenedMaterialProperties)

    @property
    def ltca_load_case_modifiable_settings(
        self: "CastSelf",
    ) -> "_1162.LTCALoadCaseModifiableSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1162

        return self.__parent__._cast(_1162.LTCALoadCaseModifiableSettings)

    @property
    def ltca_settings(self: "CastSelf") -> "_1163.LTCASettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1163

        return self.__parent__._cast(_1163.LTCASettings)

    @property
    def micropitting(self: "CastSelf") -> "_1166.Micropitting":
        from mastapy._private.gears.gear_designs.cylindrical import _1166

        return self.__parent__._cast(_1166.Micropitting)

    @property
    def muller_residual_stress_definition(
        self: "CastSelf",
    ) -> "_1167.MullerResidualStressDefinition":
        from mastapy._private.gears.gear_designs.cylindrical import _1167

        return self.__parent__._cast(_1167.MullerResidualStressDefinition)

    @property
    def scuffing(self: "CastSelf") -> "_1176.Scuffing":
        from mastapy._private.gears.gear_designs.cylindrical import _1176

        return self.__parent__._cast(_1176.Scuffing)

    @property
    def surface_roughness(self: "CastSelf") -> "_1184.SurfaceRoughness":
        from mastapy._private.gears.gear_designs.cylindrical import _1184

        return self.__parent__._cast(_1184.SurfaceRoughness)

    @property
    def tiff_analysis_settings(self: "CastSelf") -> "_1186.TiffAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1186

        return self.__parent__._cast(_1186.TiffAnalysisSettings)

    @property
    def tooth_flank_fracture_analysis_settings(
        self: "CastSelf",
    ) -> "_1190.ToothFlankFractureAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1190

        return self.__parent__._cast(_1190.ToothFlankFractureAnalysisSettings)

    @property
    def usage(self: "CastSelf") -> "_1194.Usage":
        from mastapy._private.gears.gear_designs.cylindrical import _1194

        return self.__parent__._cast(_1194.Usage)

    @property
    def eccentricity(self: "CastSelf") -> "_1378.Eccentricity":
        from mastapy._private.electric_machines import _1378

        return self.__parent__._cast(_1378.Eccentricity)

    @property
    def temperatures(self: "CastSelf") -> "_1552.Temperatures":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1552

        return self.__parent__._cast(_1552.Temperatures)

    @property
    def lookup_table_base(self: "CastSelf") -> "_1740.LookupTableBase":
        from mastapy._private.math_utility.measured_data import _1740

        return self.__parent__._cast(_1740.LookupTableBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1741.OnedimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1741

        return self.__parent__._cast(_1741.OnedimensionalFunctionLookupTable)

    @property
    def twodimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1742.TwodimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1742

        return self.__parent__._cast(_1742.TwodimensionalFunctionLookupTable)

    @property
    def skf_loss_moment_multipliers(
        self: "CastSelf",
    ) -> "_1774.SKFLossMomentMultipliers":
        from mastapy._private.utility import _1774

        return self.__parent__._cast(_1774.SKFLossMomentMultipliers)

    @property
    def roundness_specification(self: "CastSelf") -> "_2104.RoundnessSpecification":
        from mastapy._private.bearings.tolerances import _2104

        return self.__parent__._cast(_2104.RoundnessSpecification)

    @property
    def equivalent_load_factors(self: "CastSelf") -> "_2132.EquivalentLoadFactors":
        from mastapy._private.bearings.bearing_results import _2132

        return self.__parent__._cast(_2132.EquivalentLoadFactors)

    @property
    def iso14179_settings_per_bearing_type(
        self: "CastSelf",
    ) -> "_2164.ISO14179SettingsPerBearingType":
        from mastapy._private.bearings.bearing_results.rolling import _2164

        return self.__parent__._cast(_2164.ISO14179SettingsPerBearingType)

    @property
    def rolling_bearing_friction_coefficients(
        self: "CastSelf",
    ) -> "_2260.RollingBearingFrictionCoefficients":
        from mastapy._private.bearings.bearing_results.rolling import _2260

        return self.__parent__._cast(_2260.RollingBearingFrictionCoefficients)

    @property
    def additional_acceleration_options(
        self: "CastSelf",
    ) -> "_7637.AdditionalAccelerationOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7637,
        )

        return self.__parent__._cast(_7637.AdditionalAccelerationOptions)

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "IndependentReportablePropertiesBase":
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
class IndependentReportablePropertiesBase(_0.APIBase, Generic[T]):
    """IndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_REPORTABLE_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentReportablePropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_IndependentReportablePropertiesBase
        """
        return _Cast_IndependentReportablePropertiesBase(self)
