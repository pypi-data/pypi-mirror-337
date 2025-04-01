"""GearSetImplementationAnalysisAbstract"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1339

_GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationAnalysisAbstract"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1330, _1341, _1343
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214
    from mastapy._private.gears.ltca import _942
    from mastapy._private.gears.ltca.conical import _964
    from mastapy._private.gears.ltca.cylindrical import _956, _958
    from mastapy._private.gears.manufacturing.bevel import _886
    from mastapy._private.gears.manufacturing.cylindrical import _716, _717

    Self = TypeVar("Self", bound="GearSetImplementationAnalysisAbstract")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationAnalysisAbstract._Cast_GearSetImplementationAnalysisAbstract",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationAnalysisAbstract",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationAnalysisAbstract:
    """Special nested class for casting GearSetImplementationAnalysisAbstract to subclasses."""

    __parent__: "GearSetImplementationAnalysisAbstract"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1339.GearSetDesignAnalysis":
        return self.__parent__._cast(_1339.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1330.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1330

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
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_886.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _886

        return self.__parent__._cast(_886.ConicalSetManufacturingAnalysis)

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
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1214.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214

        return self.__parent__._cast(_1214.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1341.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1343.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1343

        return self.__parent__._cast(_1343.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "GearSetImplementationAnalysisAbstract":
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
class GearSetImplementationAnalysisAbstract(_1339.GearSetDesignAnalysis):
    """GearSetImplementationAnalysisAbstract

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationAnalysisAbstract":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationAnalysisAbstract
        """
        return _Cast_GearSetImplementationAnalysisAbstract(self)
