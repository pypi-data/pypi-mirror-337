"""AbstractGearAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1331, _1332, _1333, _1334
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
    from mastapy._private.gears.rating import _437, _441, _445
    from mastapy._private.gears.rating.agma_gleason_conical import _650
    from mastapy._private.gears.rating.bevel import _639
    from mastapy._private.gears.rating.concept import _632, _635
    from mastapy._private.gears.rating.conical import _622, _624
    from mastapy._private.gears.rating.cylindrical import _539, _544
    from mastapy._private.gears.rating.face import _529, _532
    from mastapy._private.gears.rating.hypoid import _523
    from mastapy._private.gears.rating.klingelnberg_conical import _496
    from mastapy._private.gears.rating.klingelnberg_hypoid import _493
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _490
    from mastapy._private.gears.rating.spiral_bevel import _487
    from mastapy._private.gears.rating.straight_bevel import _480
    from mastapy._private.gears.rating.straight_bevel_diff import _483
    from mastapy._private.gears.rating.worm import _456, _458
    from mastapy._private.gears.rating.zerol_bevel import _454

    Self = TypeVar("Self", bound="AbstractGearAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearAnalysis._Cast_AbstractGearAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearAnalysis:
    """Special nested class for casting AbstractGearAnalysis to subclasses."""

    __parent__: "AbstractGearAnalysis"

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_437.AbstractGearRating":
        from mastapy._private.gears.rating import _437

        return self.__parent__._cast(_437.AbstractGearRating)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_441.GearDutyCycleRating":
        from mastapy._private.gears.rating import _441

        return self.__parent__._cast(_441.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_445.GearRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_454.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _454

        return self.__parent__._cast(_454.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_456.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _456

        return self.__parent__._cast(_456.WormGearDutyCycleRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_458.WormGearRating":
        from mastapy._private.gears.rating.worm import _458

        return self.__parent__._cast(_458.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_480.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _480

        return self.__parent__._cast(_480.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_483.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _483

        return self.__parent__._cast(_483.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_487.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _487

        return self.__parent__._cast(_487.SpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_490.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _490

        return self.__parent__._cast(_490.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_493.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _493

        return self.__parent__._cast(_493.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "_496.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _496

        return self.__parent__._cast(_496.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_523.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _523

        return self.__parent__._cast(_523.HypoidGearRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_529.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _529

        return self.__parent__._cast(_529.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_532.FaceGearRating":
        from mastapy._private.gears.rating.face import _532

        return self.__parent__._cast(_532.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_539.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _539

        return self.__parent__._cast(_539.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_544.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _544

        return self.__parent__._cast(_544.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_622.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _622

        return self.__parent__._cast(_622.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_624.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _624

        return self.__parent__._cast(_624.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_632.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _632

        return self.__parent__._cast(_632.ConceptGearDutyCycleRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_635.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _635

        return self.__parent__._cast(_635.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_639.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _639

        return self.__parent__._cast(_639.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_650.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _650

        return self.__parent__._cast(_650.AGMAGleasonConicalGearRating)

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
    def gear_design_analysis(self: "CastSelf") -> "_1331.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1331

        return self.__parent__._cast(_1331.GearDesignAnalysis)

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
    def abstract_gear_analysis(self: "CastSelf") -> "AbstractGearAnalysis":
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
class AbstractGearAnalysis(_0.APIBase):
    """AbstractGearAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_ANALYSIS

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
    def name_with_gear_set_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NameWithGearSetName")

        if temp is None:
            return ""

        return temp

    @property
    def planet_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PlanetIndex")

        if temp is None:
            return 0

        return temp

    @planet_index.setter
    @enforce_parameter_types
    def planet_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PlanetIndex", int(value) if value is not None else 0
        )

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearAnalysis
        """
        return _Cast_AbstractGearAnalysis(self)
