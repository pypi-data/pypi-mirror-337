"""GearDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1328

_GEAR_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1332, _1333, _1334
    from mastapy._private.gears.fe_model import _1310
    from mastapy._private.gears.fe_model.conical import _1317
    from mastapy._private.gears.fe_model.cylindrical import _1314
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1206,
        _1207,
        _1208,
        _1210,
    )
    from mastapy._private.gears.gear_designs.face import _1090
    from mastapy._private.gears.gear_two_d_fe_analysis import _994, _995
    from mastapy._private.gears.load_case import _969
    from mastapy._private.gears.load_case.bevel import _987
    from mastapy._private.gears.load_case.concept import _984
    from mastapy._private.gears.load_case.conical import _981
    from mastapy._private.gears.load_case.cylindrical import _978
    from mastapy._private.gears.load_case.face import _975
    from mastapy._private.gears.load_case.worm import _972
    from mastapy._private.gears.ltca import _936
    from mastapy._private.gears.ltca.conical import _963
    from mastapy._private.gears.ltca.cylindrical import _952
    from mastapy._private.gears.manufacturing.bevel import (
        _871,
        _872,
        _873,
        _874,
        _884,
        _885,
        _890,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _708, _712, _713

    Self = TypeVar("Self", bound="GearDesignAnalysis")
    CastSelf = TypeVar("CastSelf", bound="GearDesignAnalysis._Cast_GearDesignAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignAnalysis:
    """Special nested class for casting GearDesignAnalysis to subclasses."""

    __parent__: "GearDesignAnalysis"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1328.AbstractGearAnalysis":
        return self.__parent__._cast(_1328.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_708.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _708

        return self.__parent__._cast(_708.CylindricalGearManufacturingConfig)

    @property
    def cylindrical_manufactured_gear_duty_cycle(
        self: "CastSelf",
    ) -> "_712.CylindricalManufacturedGearDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _712

        return self.__parent__._cast(_712.CylindricalManufacturedGearDutyCycle)

    @property
    def cylindrical_manufactured_gear_load_case(
        self: "CastSelf",
    ) -> "_713.CylindricalManufacturedGearLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _713

        return self.__parent__._cast(_713.CylindricalManufacturedGearLoadCase)

    @property
    def conical_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_871.ConicalGearManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _871

        return self.__parent__._cast(_871.ConicalGearManufacturingAnalysis)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_872.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _872

        return self.__parent__._cast(_872.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_873.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _873

        return self.__parent__._cast(_873.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_874.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _874

        return self.__parent__._cast(_874.ConicalGearMicroGeometryConfigBase)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_884.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _884

        return self.__parent__._cast(_884.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_885.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _885

        return self.__parent__._cast(_885.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_890.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _890

        return self.__parent__._cast(_890.ConicalWheelManufacturingConfig)

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_936.GearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _936

        return self.__parent__._cast(_936.GearLoadDistributionAnalysis)

    @property
    def cylindrical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_952.CylindricalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _952

        return self.__parent__._cast(_952.CylindricalGearLoadDistributionAnalysis)

    @property
    def conical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_963.ConicalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _963

        return self.__parent__._cast(_963.ConicalGearLoadDistributionAnalysis)

    @property
    def gear_load_case_base(self: "CastSelf") -> "_969.GearLoadCaseBase":
        from mastapy._private.gears.load_case import _969

        return self.__parent__._cast(_969.GearLoadCaseBase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_972.WormGearLoadCase":
        from mastapy._private.gears.load_case.worm import _972

        return self.__parent__._cast(_972.WormGearLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_975.FaceGearLoadCase":
        from mastapy._private.gears.load_case.face import _975

        return self.__parent__._cast(_975.FaceGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_978.CylindricalGearLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _978

        return self.__parent__._cast(_978.CylindricalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_981.ConicalGearLoadCase":
        from mastapy._private.gears.load_case.conical import _981

        return self.__parent__._cast(_981.ConicalGearLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_984.ConceptGearLoadCase":
        from mastapy._private.gears.load_case.concept import _984

        return self.__parent__._cast(_984.ConceptGearLoadCase)

    @property
    def bevel_load_case(self: "CastSelf") -> "_987.BevelLoadCase":
        from mastapy._private.gears.load_case.bevel import _987

        return self.__parent__._cast(_987.BevelLoadCase)

    @property
    def cylindrical_gear_tiff_analysis(
        self: "CastSelf",
    ) -> "_994.CylindricalGearTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _994

        return self.__parent__._cast(_994.CylindricalGearTIFFAnalysis)

    @property
    def cylindrical_gear_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_995.CylindricalGearTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _995

        return self.__parent__._cast(_995.CylindricalGearTIFFAnalysisDutyCycle)

    @property
    def face_gear_micro_geometry(self: "CastSelf") -> "_1090.FaceGearMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1090

        return self.__parent__._cast(_1090.FaceGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "_1206.CylindricalGearMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1206

        return self.__parent__._cast(_1206.CylindricalGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1207.CylindricalGearMicroGeometryBase":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1207

        return self.__parent__._cast(_1207.CylindricalGearMicroGeometryBase)

    @property
    def cylindrical_gear_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1208.CylindricalGearMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1208

        return self.__parent__._cast(_1208.CylindricalGearMicroGeometryDutyCycle)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "_1210.CylindricalGearMicroGeometryPerTooth":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1210

        return self.__parent__._cast(_1210.CylindricalGearMicroGeometryPerTooth)

    @property
    def gear_fe_model(self: "CastSelf") -> "_1310.GearFEModel":
        from mastapy._private.gears.fe_model import _1310

        return self.__parent__._cast(_1310.GearFEModel)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1314.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1314

        return self.__parent__._cast(_1314.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1317.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1317

        return self.__parent__._cast(_1317.ConicalGearFEModel)

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1332.GearImplementationAnalysis":
        from mastapy._private.gears.analysis import _1332

        return self.__parent__._cast(_1332.GearImplementationAnalysis)

    @property
    def gear_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1333.GearImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1333

        return self.__parent__._cast(_1333.GearImplementationAnalysisDutyCycle)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1334.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1334

        return self.__parent__._cast(_1334.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "GearDesignAnalysis":
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
class GearDesignAnalysis(_1328.AbstractGearAnalysis):
    """GearDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearDesignAnalysis
        """
        return _Cast_GearDesignAnalysis(self)
