"""CustomDrawing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1930

_CUSTOM_DRAWING = python_net_import("SMT.MastaAPI.Utility.Report", "CustomDrawing")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1938, _1941, _1949

    Self = TypeVar("Self", bound="CustomDrawing")
    CastSelf = TypeVar("CastSelf", bound="CustomDrawing._Cast_CustomDrawing")


__docformat__ = "restructuredtext en"
__all__ = ("CustomDrawing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomDrawing:
    """Special nested class for casting CustomDrawing to subclasses."""

    __parent__: "CustomDrawing"

    @property
    def custom_graphic(self: "CastSelf") -> "_1930.CustomGraphic":
        return self.__parent__._cast(_1930.CustomGraphic)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1938.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1938

        return self.__parent__._cast(_1938.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1949.CustomReportNameableItem":
        from mastapy._private.utility.report import _1949

        return self.__parent__._cast(_1949.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1941.CustomReportItem":
        from mastapy._private.utility.report import _1941

        return self.__parent__._cast(_1941.CustomReportItem)

    @property
    def custom_drawing(self: "CastSelf") -> "CustomDrawing":
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
class CustomDrawing(_1930.CustomGraphic):
    """CustomDrawing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_DRAWING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def show_editor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowEditor")

        if temp is None:
            return False

        return temp

    @show_editor.setter
    @enforce_parameter_types
    def show_editor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowEditor", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomDrawing":
        """Cast to another type.

        Returns:
            _Cast_CustomDrawing
        """
        return _Cast_CustomDrawing(self)
