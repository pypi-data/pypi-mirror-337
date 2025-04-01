"""AbstractGearSetAnalysis"""

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

_ABSTRACT_GEAR_SET_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearSetAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1339, _1341, _1342, _1343, _1344
    from mastapy._private.gears.fe_model import _1313
    from mastapy._private.gears.fe_model.conical import _1319
    from mastapy._private.gears.fe_model.cylindrical import _1316
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1213,
        _1214,
    )
    from mastapy._private.gears.gear_designs.face import _1093
    from mastapy._private.gears.gear_two_d_fe_analysis import _992, _993
    from mastapy._private.gears.load_case import _970
    from mastapy._private.gears.load_case.bevel import _989
    from mastapy._private.gears.load_case.concept import _985
    from mastapy._private.gears.load_case.conical import _982
    from mastapy._private.gears.load_case.cylindrical import _979
    from mastapy._private.gears.load_case.face import _976
    from mastapy._private.gears.load_case.worm import _973
    from mastapy._private.gears.ltca import _942
    from mastapy._private.gears.ltca.conical import _964
    from mastapy._private.gears.ltca.cylindrical import _956, _958
    from mastapy._private.gears.manufacturing.bevel import _886, _887, _888, _889
    from mastapy._private.gears.manufacturing.cylindrical import _716, _717, _721
    from mastapy._private.gears.rating import _438, _446, _447
    from mastapy._private.gears.rating.agma_gleason_conical import _651
    from mastapy._private.gears.rating.bevel import _640
    from mastapy._private.gears.rating.concept import _636, _637
    from mastapy._private.gears.rating.conical import _625, _626
    from mastapy._private.gears.rating.cylindrical import _547, _548, _564
    from mastapy._private.gears.rating.face import _533, _534
    from mastapy._private.gears.rating.hypoid import _524
    from mastapy._private.gears.rating.klingelnberg_conical import _497
    from mastapy._private.gears.rating.klingelnberg_hypoid import _494
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _491
    from mastapy._private.gears.rating.spiral_bevel import _488
    from mastapy._private.gears.rating.straight_bevel import _481
    from mastapy._private.gears.rating.straight_bevel_diff import _484
    from mastapy._private.gears.rating.worm import _459, _460
    from mastapy._private.gears.rating.zerol_bevel import _455
    from mastapy._private.utility.model_validation import _1971, _1972

    Self = TypeVar("Self", bound="AbstractGearSetAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearSetAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearSetAnalysis:
    """Special nested class for casting AbstractGearSetAnalysis to subclasses."""

    __parent__: "AbstractGearSetAnalysis"

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_438.AbstractGearSetRating":
        from mastapy._private.gears.rating import _438

        return self.__parent__._cast(_438.AbstractGearSetRating)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_446.GearSetDutyCycleRating":
        from mastapy._private.gears.rating import _446

        return self.__parent__._cast(_446.GearSetDutyCycleRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_447.GearSetRating":
        from mastapy._private.gears.rating import _447

        return self.__parent__._cast(_447.GearSetRating)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_455.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _455

        return self.__parent__._cast(_455.ZerolBevelGearSetRating)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_459.WormGearSetDutyCycleRating":
        from mastapy._private.gears.rating.worm import _459

        return self.__parent__._cast(_459.WormGearSetDutyCycleRating)

    @property
    def worm_gear_set_rating(self: "CastSelf") -> "_460.WormGearSetRating":
        from mastapy._private.gears.rating.worm import _460

        return self.__parent__._cast(_460.WormGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_481.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _481

        return self.__parent__._cast(_481.StraightBevelGearSetRating)

    @property
    def straight_bevel_diff_gear_set_rating(
        self: "CastSelf",
    ) -> "_484.StraightBevelDiffGearSetRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _484

        return self.__parent__._cast(_484.StraightBevelDiffGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_488.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _488

        return self.__parent__._cast(_488.SpiralBevelGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_491.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _491

        return self.__parent__._cast(
            _491.KlingelnbergCycloPalloidSpiralBevelGearSetRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "_494.KlingelnbergCycloPalloidHypoidGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _494

        return self.__parent__._cast(_494.KlingelnbergCycloPalloidHypoidGearSetRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_497.KlingelnbergCycloPalloidConicalGearSetRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _497

        return self.__parent__._cast(_497.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def hypoid_gear_set_rating(self: "CastSelf") -> "_524.HypoidGearSetRating":
        from mastapy._private.gears.rating.hypoid import _524

        return self.__parent__._cast(_524.HypoidGearSetRating)

    @property
    def face_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_533.FaceGearSetDutyCycleRating":
        from mastapy._private.gears.rating.face import _533

        return self.__parent__._cast(_533.FaceGearSetDutyCycleRating)

    @property
    def face_gear_set_rating(self: "CastSelf") -> "_534.FaceGearSetRating":
        from mastapy._private.gears.rating.face import _534

        return self.__parent__._cast(_534.FaceGearSetRating)

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_547.CylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _547

        return self.__parent__._cast(_547.CylindricalGearSetDutyCycleRating)

    @property
    def cylindrical_gear_set_rating(
        self: "CastSelf",
    ) -> "_548.CylindricalGearSetRating":
        from mastapy._private.gears.rating.cylindrical import _548

        return self.__parent__._cast(_548.CylindricalGearSetRating)

    @property
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_564.ReducedCylindricalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _564

        return self.__parent__._cast(_564.ReducedCylindricalGearSetDutyCycleRating)

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_625.ConicalGearSetDutyCycleRating":
        from mastapy._private.gears.rating.conical import _625

        return self.__parent__._cast(_625.ConicalGearSetDutyCycleRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_626.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _626

        return self.__parent__._cast(_626.ConicalGearSetRating)

    @property
    def concept_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_636.ConceptGearSetDutyCycleRating":
        from mastapy._private.gears.rating.concept import _636

        return self.__parent__._cast(_636.ConceptGearSetDutyCycleRating)

    @property
    def concept_gear_set_rating(self: "CastSelf") -> "_637.ConceptGearSetRating":
        from mastapy._private.gears.rating.concept import _637

        return self.__parent__._cast(_637.ConceptGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_640.BevelGearSetRating":
        from mastapy._private.gears.rating.bevel import _640

        return self.__parent__._cast(_640.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_651.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _651

        return self.__parent__._cast(_651.AGMAGleasonConicalGearSetRating)

    @property
    def cylindrical_manufactured_gear_set_duty_cycle(
        self: "CastSelf",
    ) -> "_716.CylindricalManufacturedGearSetDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _716

        return self.__parent__._cast(_716.CylindricalManufacturedGearSetDutyCycle)

    @property
    def cylindrical_manufactured_gear_set_load_case(
        self: "CastSelf",
    ) -> "_717.CylindricalManufacturedGearSetLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _717

        return self.__parent__._cast(_717.CylindricalManufacturedGearSetLoadCase)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_721.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _721

        return self.__parent__._cast(_721.CylindricalSetManufacturingConfig)

    @property
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_886.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _886

        return self.__parent__._cast(_886.ConicalSetManufacturingAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_887.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _887

        return self.__parent__._cast(_887.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_888.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _888

        return self.__parent__._cast(_888.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_889.ConicalSetMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _889

        return self.__parent__._cast(_889.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_942.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _942

        return self.__parent__._cast(_942.GearSetLoadDistributionAnalysis)

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_956.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _956

        return self.__parent__._cast(_956.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_958.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _958

        return self.__parent__._cast(_958.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_964.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _964

        return self.__parent__._cast(_964.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_970.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _970

        return self.__parent__._cast(_970.GearSetLoadCaseBase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_973.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _973

        return self.__parent__._cast(_973.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_976.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _976

        return self.__parent__._cast(_976.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_979.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _979

        return self.__parent__._cast(_979.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_982.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _982

        return self.__parent__._cast(_982.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_985.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _985

        return self.__parent__._cast(_985.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_989.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _989

        return self.__parent__._cast(_989.BevelSetLoadCase)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "_992.CylindricalGearSetTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _992

        return self.__parent__._cast(_992.CylindricalGearSetTIFFAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_993.CylindricalGearSetTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _993

        return self.__parent__._cast(_993.CylindricalGearSetTIFFAnalysisDutyCycle)

    @property
    def face_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1093.FaceGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1093

        return self.__parent__._cast(_1093.FaceGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1213.CylindricalGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1213

        return self.__parent__._cast(_1213.CylindricalGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1214.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214

        return self.__parent__._cast(_1214.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1313.GearSetFEModel":
        from mastapy._private.gears.fe_model import _1313

        return self.__parent__._cast(_1313.GearSetFEModel)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1316.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1316

        return self.__parent__._cast(_1316.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1319.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1319

        return self.__parent__._cast(_1319.ConicalSetFEModel)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1339.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1339

        return self.__parent__._cast(_1339.GearSetDesignAnalysis)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1341.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1342.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1343.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1343

        return self.__parent__._cast(_1343.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1344.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1344

        return self.__parent__._cast(_1344.GearSetImplementationDetail)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "AbstractGearSetAnalysis":
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
class AbstractGearSetAnalysis(_0.APIBase):
    """AbstractGearSetAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_SET_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearSetAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearSetAnalysis
        """
        return _Cast_AbstractGearSetAnalysis(self)
