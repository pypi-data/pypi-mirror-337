"""GearMeshImplementationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1335

_GEAR_MESH_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1329
    from mastapy._private.gears.fe_model import _1311
    from mastapy._private.gears.fe_model.conical import _1318
    from mastapy._private.gears.fe_model.cylindrical import _1315
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1204
    from mastapy._private.gears.gear_designs.face import _1089
    from mastapy._private.gears.manufacturing.bevel import _881, _882, _883
    from mastapy._private.gears.manufacturing.cylindrical import _718

    Self = TypeVar("Self", bound="GearMeshImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshImplementationDetail._Cast_GearMeshImplementationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshImplementationDetail:
    """Special nested class for casting GearMeshImplementationDetail to subclasses."""

    __parent__: "GearMeshImplementationDetail"

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1335.GearMeshDesignAnalysis":
        return self.__parent__._cast(_1335.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1329.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1329

        return self.__parent__._cast(_1329.AbstractGearMeshAnalysis)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_718.CylindricalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _718

        return self.__parent__._cast(_718.CylindricalMeshManufacturingConfig)

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
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "GearMeshImplementationDetail":
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
class GearMeshImplementationDetail(_1335.GearMeshDesignAnalysis):
    """GearMeshImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_IMPLEMENTATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearMeshImplementationDetail
        """
        return _Cast_GearMeshImplementationDetail(self)
