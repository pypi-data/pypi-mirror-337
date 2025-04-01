"""GearSetImplementationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1339

_GEAR_SET_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1330
    from mastapy._private.gears.fe_model import _1313
    from mastapy._private.gears.fe_model.conical import _1319
    from mastapy._private.gears.fe_model.cylindrical import _1316
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1213
    from mastapy._private.gears.gear_designs.face import _1093
    from mastapy._private.gears.manufacturing.bevel import _887, _888, _889
    from mastapy._private.gears.manufacturing.cylindrical import _721
    from mastapy._private.utility.scripting import _1919

    Self = TypeVar("Self", bound="GearSetImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationDetail._Cast_GearSetImplementationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationDetail:
    """Special nested class for casting GearSetImplementationDetail to subclasses."""

    __parent__: "GearSetImplementationDetail"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1339.GearSetDesignAnalysis":
        return self.__parent__._cast(_1339.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1330.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1330

        return self.__parent__._cast(_1330.AbstractGearSetAnalysis)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_721.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _721

        return self.__parent__._cast(_721.CylindricalSetManufacturingConfig)

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
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "GearSetImplementationDetail":
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
class GearSetImplementationDetail(_1339.GearSetDesignAnalysis):
    """GearSetImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_DETAIL

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
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationDetail
        """
        return _Cast_GearSetImplementationDetail(self)
