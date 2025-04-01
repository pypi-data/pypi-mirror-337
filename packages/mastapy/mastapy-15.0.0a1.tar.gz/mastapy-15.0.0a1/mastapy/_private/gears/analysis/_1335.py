"""GearMeshDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1329

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1331, _1336, _1337, _1338, _1339
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

    Self = TypeVar("Self", bound="GearMeshDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshDesignAnalysis._Cast_GearMeshDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDesignAnalysis:
    """Special nested class for casting GearMeshDesignAnalysis to subclasses."""

    __parent__: "GearMeshDesignAnalysis"

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1329.AbstractGearMeshAnalysis":
        return self.__parent__._cast(_1329.AbstractGearMeshAnalysis)

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
    def gear_mesh_design_analysis(self: "CastSelf") -> "GearMeshDesignAnalysis":
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
class GearMeshDesignAnalysis(_1329.AbstractGearMeshAnalysis):
    """GearMeshDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_a(self: "Self") -> "_1331.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_b(self: "Self") -> "_1331.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set(self: "Self") -> "_1339.GearSetDesignAnalysis":
        """mastapy.gears.analysis.GearSetDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDesignAnalysis
        """
        return _Cast_GearMeshDesignAnalysis(self)
