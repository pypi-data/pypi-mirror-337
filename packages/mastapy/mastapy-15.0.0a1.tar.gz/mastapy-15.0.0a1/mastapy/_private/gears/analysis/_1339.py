"""GearSetDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1330

_GEAR_SET_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1341, _1342, _1343, _1344
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

    Self = TypeVar("Self", bound="GearSetDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetDesignAnalysis._Cast_GearSetDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesignAnalysis:
    """Special nested class for casting GearSetDesignAnalysis to subclasses."""

    __parent__: "GearSetDesignAnalysis"

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1330.AbstractGearSetAnalysis":
        return self.__parent__._cast(_1330.AbstractGearSetAnalysis)

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
    def gear_set_design_analysis(self: "CastSelf") -> "GearSetDesignAnalysis":
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
class GearSetDesignAnalysis(_1330.AbstractGearSetAnalysis):
    """GearSetDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesignAnalysis
        """
        return _Cast_GearSetDesignAnalysis(self)
