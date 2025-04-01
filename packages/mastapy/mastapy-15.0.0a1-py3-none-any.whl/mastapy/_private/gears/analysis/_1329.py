"""AbstractGearMeshAnalysis"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_MESH_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearMeshAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1328, _1335, _1336, _1337, _1338
    from mastapy._private.gears.fe_model import _1311
    from mastapy._private.gears.fe_model.conical import _1318
    from mastapy._private.gears.fe_model.cylindrical import _1315
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1204,
        _1205,
    )
    from mastapy._private.gears.gear_designs.face import _1089
    from mastapy._private.gears.gear_two_d_fe_analysis import _990, _991
    from mastapy._private.gears.load_case import _971
    from mastapy._private.gears.load_case.bevel import _988
    from mastapy._private.gears.load_case.concept import _986
    from mastapy._private.gears.load_case.conical import _983
    from mastapy._private.gears.load_case.cylindrical import _980
    from mastapy._private.gears.load_case.face import _977
    from mastapy._private.gears.load_case.worm import _974
    from mastapy._private.gears.ltca import _937
    from mastapy._private.gears.ltca.conical import _966
    from mastapy._private.gears.ltca.cylindrical import _953
    from mastapy._private.gears.manufacturing.bevel import _880, _881, _882, _883
    from mastapy._private.gears.manufacturing.cylindrical import _714, _715, _718
    from mastapy._private.gears.rating import _436, _444, _449
    from mastapy._private.gears.rating.agma_gleason_conical import _649
    from mastapy._private.gears.rating.bevel import _638
    from mastapy._private.gears.rating.concept import _633, _634
    from mastapy._private.gears.rating.conical import _623, _628
    from mastapy._private.gears.rating.cylindrical import _542, _550
    from mastapy._private.gears.rating.face import _530, _531
    from mastapy._private.gears.rating.hypoid import _522
    from mastapy._private.gears.rating.klingelnberg_conical import _495
    from mastapy._private.gears.rating.klingelnberg_hypoid import _492
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _489
    from mastapy._private.gears.rating.spiral_bevel import _486
    from mastapy._private.gears.rating.straight_bevel import _479
    from mastapy._private.gears.rating.straight_bevel_diff import _482
    from mastapy._private.gears.rating.worm import _457, _461
    from mastapy._private.gears.rating.zerol_bevel import _453

    Self = TypeVar("Self", bound="AbstractGearMeshAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearMeshAnalysis._Cast_AbstractGearMeshAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearMeshAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearMeshAnalysis:
    """Special nested class for casting AbstractGearMeshAnalysis to subclasses."""

    __parent__: "AbstractGearMeshAnalysis"

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_436.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _436

        return self.__parent__._cast(_436.AbstractGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_444.GearMeshRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.GearMeshRating)

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_449.MeshDutyCycleRating":
        from mastapy._private.gears.rating import _449

        return self.__parent__._cast(_449.MeshDutyCycleRating)

    @property
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_453.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _453

        return self.__parent__._cast(_453.ZerolBevelGearMeshRating)

    @property
    def worm_gear_mesh_rating(self: "CastSelf") -> "_457.WormGearMeshRating":
        from mastapy._private.gears.rating.worm import _457

        return self.__parent__._cast(_457.WormGearMeshRating)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "_461.WormMeshDutyCycleRating":
        from mastapy._private.gears.rating.worm import _461

        return self.__parent__._cast(_461.WormMeshDutyCycleRating)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_479.StraightBevelGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel import _479

        return self.__parent__._cast(_479.StraightBevelGearMeshRating)

    @property
    def straight_bevel_diff_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_482.StraightBevelDiffGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _482

        return self.__parent__._cast(_482.StraightBevelDiffGearMeshRating)

    @property
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_486.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _486

        return self.__parent__._cast(_486.SpiralBevelGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_489.KlingelnbergCycloPalloidSpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _489

        return self.__parent__._cast(
            _489.KlingelnbergCycloPalloidSpiralBevelGearMeshRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_492.KlingelnbergCycloPalloidHypoidGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _492

        return self.__parent__._cast(_492.KlingelnbergCycloPalloidHypoidGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_495.KlingelnbergCycloPalloidConicalGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _495

        return self.__parent__._cast(_495.KlingelnbergCycloPalloidConicalGearMeshRating)

    @property
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "_522.HypoidGearMeshRating":
        from mastapy._private.gears.rating.hypoid import _522

        return self.__parent__._cast(_522.HypoidGearMeshRating)

    @property
    def face_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_530.FaceGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.face import _530

        return self.__parent__._cast(_530.FaceGearMeshDutyCycleRating)

    @property
    def face_gear_mesh_rating(self: "CastSelf") -> "_531.FaceGearMeshRating":
        from mastapy._private.gears.rating.face import _531

        return self.__parent__._cast(_531.FaceGearMeshRating)

    @property
    def cylindrical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_542.CylindricalGearMeshRating":
        from mastapy._private.gears.rating.cylindrical import _542

        return self.__parent__._cast(_542.CylindricalGearMeshRating)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_550.CylindricalMeshDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _550

        return self.__parent__._cast(_550.CylindricalMeshDutyCycleRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_623.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _623

        return self.__parent__._cast(_623.ConicalGearMeshRating)

    @property
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_628.ConicalMeshDutyCycleRating":
        from mastapy._private.gears.rating.conical import _628

        return self.__parent__._cast(_628.ConicalMeshDutyCycleRating)

    @property
    def concept_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_633.ConceptGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.concept import _633

        return self.__parent__._cast(_633.ConceptGearMeshDutyCycleRating)

    @property
    def concept_gear_mesh_rating(self: "CastSelf") -> "_634.ConceptGearMeshRating":
        from mastapy._private.gears.rating.concept import _634

        return self.__parent__._cast(_634.ConceptGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_638.BevelGearMeshRating":
        from mastapy._private.gears.rating.bevel import _638

        return self.__parent__._cast(_638.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_649.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _649

        return self.__parent__._cast(_649.AGMAGleasonConicalGearMeshRating)

    @property
    def cylindrical_manufactured_gear_mesh_duty_cycle(
        self: "CastSelf",
    ) -> "_714.CylindricalManufacturedGearMeshDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _714

        return self.__parent__._cast(_714.CylindricalManufacturedGearMeshDutyCycle)

    @property
    def cylindrical_manufactured_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_715.CylindricalManufacturedGearMeshLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _715

        return self.__parent__._cast(_715.CylindricalManufacturedGearMeshLoadCase)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_718.CylindricalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _718

        return self.__parent__._cast(_718.CylindricalMeshManufacturingConfig)

    @property
    def conical_mesh_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_880.ConicalMeshManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _880

        return self.__parent__._cast(_880.ConicalMeshManufacturingAnalysis)

    @property
    def conical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_881.ConicalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _881

        return self.__parent__._cast(_881.ConicalMeshManufacturingConfig)

    @property
    def conical_mesh_micro_geometry_config(
        self: "CastSelf",
    ) -> "_882.ConicalMeshMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _882

        return self.__parent__._cast(_882.ConicalMeshMicroGeometryConfig)

    @property
    def conical_mesh_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_883.ConicalMeshMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _883

        return self.__parent__._cast(_883.ConicalMeshMicroGeometryConfigBase)

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_937.GearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _937

        return self.__parent__._cast(_937.GearMeshLoadDistributionAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_953.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _953

        return self.__parent__._cast(_953.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_966.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _966

        return self.__parent__._cast(_966.ConicalMeshLoadDistributionAnalysis)

    @property
    def mesh_load_case(self: "CastSelf") -> "_971.MeshLoadCase":
        from mastapy._private.gears.load_case import _971

        return self.__parent__._cast(_971.MeshLoadCase)

    @property
    def worm_mesh_load_case(self: "CastSelf") -> "_974.WormMeshLoadCase":
        from mastapy._private.gears.load_case.worm import _974

        return self.__parent__._cast(_974.WormMeshLoadCase)

    @property
    def face_mesh_load_case(self: "CastSelf") -> "_977.FaceMeshLoadCase":
        from mastapy._private.gears.load_case.face import _977

        return self.__parent__._cast(_977.FaceMeshLoadCase)

    @property
    def cylindrical_mesh_load_case(self: "CastSelf") -> "_980.CylindricalMeshLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _980

        return self.__parent__._cast(_980.CylindricalMeshLoadCase)

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "_983.ConicalMeshLoadCase":
        from mastapy._private.gears.load_case.conical import _983

        return self.__parent__._cast(_983.ConicalMeshLoadCase)

    @property
    def concept_mesh_load_case(self: "CastSelf") -> "_986.ConceptMeshLoadCase":
        from mastapy._private.gears.load_case.concept import _986

        return self.__parent__._cast(_986.ConceptMeshLoadCase)

    @property
    def bevel_mesh_load_case(self: "CastSelf") -> "_988.BevelMeshLoadCase":
        from mastapy._private.gears.load_case.bevel import _988

        return self.__parent__._cast(_988.BevelMeshLoadCase)

    @property
    def cylindrical_gear_mesh_tiff_analysis(
        self: "CastSelf",
    ) -> "_990.CylindricalGearMeshTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _990

        return self.__parent__._cast(_990.CylindricalGearMeshTIFFAnalysis)

    @property
    def cylindrical_gear_mesh_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_991.CylindricalGearMeshTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _991

        return self.__parent__._cast(_991.CylindricalGearMeshTIFFAnalysisDutyCycle)

    @property
    def face_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1089.FaceGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1089

        return self.__parent__._cast(_1089.FaceGearMeshMicroGeometry)

    @property
    def cylindrical_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1204.CylindricalGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1204

        return self.__parent__._cast(_1204.CylindricalGearMeshMicroGeometry)

    @property
    def cylindrical_gear_mesh_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1205.CylindricalGearMeshMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1205

        return self.__parent__._cast(_1205.CylindricalGearMeshMicroGeometryDutyCycle)

    @property
    def gear_mesh_fe_model(self: "CastSelf") -> "_1311.GearMeshFEModel":
        from mastapy._private.gears.fe_model import _1311

        return self.__parent__._cast(_1311.GearMeshFEModel)

    @property
    def cylindrical_gear_mesh_fe_model(
        self: "CastSelf",
    ) -> "_1315.CylindricalGearMeshFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1315

        return self.__parent__._cast(_1315.CylindricalGearMeshFEModel)

    @property
    def conical_mesh_fe_model(self: "CastSelf") -> "_1318.ConicalMeshFEModel":
        from mastapy._private.gears.fe_model.conical import _1318

        return self.__parent__._cast(_1318.ConicalMeshFEModel)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1335.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.GearMeshDesignAnalysis)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1336.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1337.GearMeshImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.GearMeshImplementationAnalysisDutyCycle)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1338.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearMeshImplementationDetail)

    @property
    def abstract_gear_mesh_analysis(self: "CastSelf") -> "AbstractGearMeshAnalysis":
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
class AbstractGearMeshAnalysis(_0.APIBase):
    """AbstractGearMeshAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_MESH_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mesh_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshName")

        if temp is None:
            return ""

        return temp

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
    def gear_a(self: "Self") -> "_1328.AbstractGearAnalysis":
        """mastapy.gears.analysis.AbstractGearAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_b(self: "Self") -> "_1328.AbstractGearAnalysis":
        """mastapy.gears.analysis.AbstractGearAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

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
    def cast_to(self: "Self") -> "_Cast_AbstractGearMeshAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearMeshAnalysis
        """
        return _Cast_AbstractGearMeshAnalysis(self)
