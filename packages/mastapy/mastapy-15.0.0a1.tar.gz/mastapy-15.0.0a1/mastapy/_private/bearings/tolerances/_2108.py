"""SupportTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.tolerances import _2095, _2096, _2109

_SUPPORT_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "SupportTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2087, _2093, _2099

    Self = TypeVar("Self", bound="SupportTolerance")
    CastSelf = TypeVar("CastSelf", bound="SupportTolerance._Cast_SupportTolerance")


__docformat__ = "restructuredtext en"
__all__ = ("SupportTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SupportTolerance:
    """Special nested class for casting SupportTolerance to subclasses."""

    __parent__: "SupportTolerance"

    @property
    def interference_tolerance(self: "CastSelf") -> "_2095.InterferenceTolerance":
        return self.__parent__._cast(_2095.InterferenceTolerance)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_2087.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _2087

        return self.__parent__._cast(_2087.BearingConnectionComponent)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_2093.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _2093

        return self.__parent__._cast(_2093.InnerSupportTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_2099.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _2099

        return self.__parent__._cast(_2099.OuterSupportTolerance)

    @property
    def support_tolerance(self: "CastSelf") -> "SupportTolerance":
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
class SupportTolerance(_2095.InterferenceTolerance):
    """SupportTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUPPORT_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def tolerance_band_designation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ITDesignation":
        """EnumWithSelectedValue[mastapy.bearings.tolerances.ITDesignation]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceBandDesignation")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_ITDesignation.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @tolerance_band_designation.setter
    @enforce_parameter_types
    def tolerance_band_designation(self: "Self", value: "_2096.ITDesignation") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToleranceBandDesignation", value)

    @property
    def tolerance_deviation_class(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation":
        """EnumWithSelectedValue[mastapy.bearings.tolerances.SupportToleranceLocationDesignation]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceDeviationClass")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @tolerance_deviation_class.setter
    @enforce_parameter_types
    def tolerance_deviation_class(
        self: "Self", value: "_2109.SupportToleranceLocationDesignation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToleranceDeviationClass", value)

    @property
    def cast_to(self: "Self") -> "_Cast_SupportTolerance":
        """Cast to another type.

        Returns:
            _Cast_SupportTolerance
        """
        return _Cast_SupportTolerance(self)
