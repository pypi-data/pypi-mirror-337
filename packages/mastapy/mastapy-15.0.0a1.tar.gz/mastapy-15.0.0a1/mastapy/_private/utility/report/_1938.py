"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1949

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2134
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4618,
    )
    from mastapy._private.utility.report import (
        _1920,
        _1928,
        _1929,
        _1930,
        _1931,
        _1940,
        _1941,
        _1952,
        _1955,
        _1957,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1949.CustomReportNameableItem":
        return self.__parent__._cast(_1949.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1941.CustomReportItem":
        from mastapy._private.utility.report import _1941

        return self.__parent__._cast(_1941.CustomReportItem)

    @property
    def ad_hoc_custom_table(self: "CastSelf") -> "_1920.AdHocCustomTable":
        from mastapy._private.utility.report import _1920

        return self.__parent__._cast(_1920.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1928.CustomChart":
        from mastapy._private.utility.report import _1928

        return self.__parent__._cast(_1928.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1929.CustomDrawing":
        from mastapy._private.utility.report import _1929

        return self.__parent__._cast(_1929.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1930.CustomGraphic":
        from mastapy._private.utility.report import _1930

        return self.__parent__._cast(_1930.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1931.CustomImage":
        from mastapy._private.utility.report import _1931

        return self.__parent__._cast(_1931.CustomImage)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1940.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1940

        return self.__parent__._cast(_1940.CustomReportHtmlItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1952.CustomReportStatusItem":
        from mastapy._private.utility.report import _1952

        return self.__parent__._cast(_1952.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1955.CustomReportText":
        from mastapy._private.utility.report import _1955

        return self.__parent__._cast(_1955.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1957.CustomSubReport":
        from mastapy._private.utility.report import _1957

        return self.__parent__._cast(_1957.CustomSubReport)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2134.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2134

        return self.__parent__._cast(_2134.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4618.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4618,
        )

        return self.__parent__._cast(_4618.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1949.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
