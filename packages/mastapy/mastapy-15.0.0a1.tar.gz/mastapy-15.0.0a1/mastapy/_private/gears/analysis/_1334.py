"""GearImplementationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1331

_GEAR_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1328
    from mastapy._private.gears.fe_model import _1310
    from mastapy._private.gears.fe_model.conical import _1317
    from mastapy._private.gears.fe_model.cylindrical import _1314
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1206,
        _1207,
        _1210,
    )
    from mastapy._private.gears.gear_designs.face import _1090
    from mastapy._private.gears.manufacturing.bevel import (
        _872,
        _873,
        _874,
        _884,
        _885,
        _890,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _708
    from mastapy._private.utility.scripting import _1919

    Self = TypeVar("Self", bound="GearImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="GearImplementationDetail._Cast_GearImplementationDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearImplementationDetail:
    """Special nested class for casting GearImplementationDetail to subclasses."""

    __parent__: "GearImplementationDetail"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1331.GearDesignAnalysis":
        return self.__parent__._cast(_1331.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1328.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1328

        return self.__parent__._cast(_1328.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_708.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _708

        return self.__parent__._cast(_708.CylindricalGearManufacturingConfig)

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
    def gear_implementation_detail(self: "CastSelf") -> "GearImplementationDetail":
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
class GearImplementationDetail(_1331.GearDesignAnalysis):
    """GearImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_IMPLEMENTATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def user_specified_data(self: "Self") -> "_1919.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearImplementationDetail
        """
        return _Cast_GearImplementationDetail(self)
