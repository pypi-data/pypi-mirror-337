"""CustomReportItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CUSTOM_REPORT_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2133, _2134, _2137, _2145
    from mastapy._private.gears.gear_designs.cylindrical import _1138
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4954,
        _4958,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4618,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3057,
    )
    from mastapy._private.utility.report import (
        _1920,
        _1928,
        _1929,
        _1930,
        _1931,
        _1932,
        _1933,
        _1934,
        _1936,
        _1937,
        _1938,
        _1939,
        _1940,
        _1942,
        _1943,
        _1944,
        _1945,
        _1947,
        _1948,
        _1949,
        _1950,
        _1952,
        _1953,
        _1954,
        _1955,
        _1957,
        _1958,
        _1960,
    )
    from mastapy._private.utility_gui.charts import _2040, _2041

    Self = TypeVar("Self", bound="CustomReportItem")
    CastSelf = TypeVar("CastSelf", bound="CustomReportItem._Cast_CustomReportItem")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportItem:
    """Special nested class for casting CustomReportItem to subclasses."""

    __parent__: "CustomReportItem"

    @property
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1138

        return self.__parent__._cast(_1138.CylindricalGearTableWithMGCharts)

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
    def custom_report(self: "CastSelf") -> "_1932.CustomReport":
        from mastapy._private.utility.report import _1932

        return self.__parent__._cast(_1932.CustomReport)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1933.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1933

        return self.__parent__._cast(_1933.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1934.CustomReportChart":
        from mastapy._private.utility.report import _1934

        return self.__parent__._cast(_1934.CustomReportChart)

    @property
    def custom_report_column(self: "CastSelf") -> "_1936.CustomReportColumn":
        from mastapy._private.utility.report import _1936

        return self.__parent__._cast(_1936.CustomReportColumn)

    @property
    def custom_report_columns(self: "CastSelf") -> "_1937.CustomReportColumns":
        from mastapy._private.utility.report import _1937

        return self.__parent__._cast(_1937.CustomReportColumns)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1938.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1938

        return self.__parent__._cast(_1938.CustomReportDefinitionItem)

    @property
    def custom_report_horizontal_line(
        self: "CastSelf",
    ) -> "_1939.CustomReportHorizontalLine":
        from mastapy._private.utility.report import _1939

        return self.__parent__._cast(_1939.CustomReportHorizontalLine)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1940.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1940

        return self.__parent__._cast(_1940.CustomReportHtmlItem)

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1942.CustomReportItemContainer":
        from mastapy._private.utility.report import _1942

        return self.__parent__._cast(_1942.CustomReportItemContainer)

    @property
    def custom_report_item_container_collection(
        self: "CastSelf",
    ) -> "_1943.CustomReportItemContainerCollection":
        from mastapy._private.utility.report import _1943

        return self.__parent__._cast(_1943.CustomReportItemContainerCollection)

    @property
    def custom_report_item_container_collection_base(
        self: "CastSelf",
    ) -> "_1944.CustomReportItemContainerCollectionBase":
        from mastapy._private.utility.report import _1944

        return self.__parent__._cast(_1944.CustomReportItemContainerCollectionBase)

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "_1945.CustomReportItemContainerCollectionItem":
        from mastapy._private.utility.report import _1945

        return self.__parent__._cast(_1945.CustomReportItemContainerCollectionItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1947.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1947

        return self.__parent__._cast(_1947.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1948.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1948

        return self.__parent__._cast(_1948.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1949.CustomReportNameableItem":
        from mastapy._private.utility.report import _1949

        return self.__parent__._cast(_1949.CustomReportNameableItem)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_1950.CustomReportNamedItem":
        from mastapy._private.utility.report import _1950

        return self.__parent__._cast(_1950.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1952.CustomReportStatusItem":
        from mastapy._private.utility.report import _1952

        return self.__parent__._cast(_1952.CustomReportStatusItem)

    @property
    def custom_report_tab(self: "CastSelf") -> "_1953.CustomReportTab":
        from mastapy._private.utility.report import _1953

        return self.__parent__._cast(_1953.CustomReportTab)

    @property
    def custom_report_tabs(self: "CastSelf") -> "_1954.CustomReportTabs":
        from mastapy._private.utility.report import _1954

        return self.__parent__._cast(_1954.CustomReportTabs)

    @property
    def custom_report_text(self: "CastSelf") -> "_1955.CustomReportText":
        from mastapy._private.utility.report import _1955

        return self.__parent__._cast(_1955.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1957.CustomSubReport":
        from mastapy._private.utility.report import _1957

        return self.__parent__._cast(_1957.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_1958.CustomTable":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_1960.DynamicCustomReportItem":
        from mastapy._private.utility.report import _1960

        return self.__parent__._cast(_1960.DynamicCustomReportItem)

    @property
    def custom_line_chart(self: "CastSelf") -> "_2040.CustomLineChart":
        from mastapy._private.utility_gui.charts import _2040

        return self.__parent__._cast(_2040.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_2041.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _2041

        return self.__parent__._cast(_2041.CustomTableAndChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2133.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2133

        return self.__parent__._cast(_2133.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2134.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2134

        return self.__parent__._cast(_2134.LoadedBearingChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2137.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2137

        return self.__parent__._cast(_2137.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2145.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2145

        return self.__parent__._cast(_2145.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_3057.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _3057,
        )

        return self.__parent__._cast(_3057.ShaftSystemDeflectionSectionsReport)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4618.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4618,
        )

        return self.__parent__._cast(_4618.ParametricStudyHistogram)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_4954.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4954,
        )

        return self.__parent__._cast(_4954.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_4958.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4958,
        )

        return self.__parent__._cast(_4958.PerModeResultsReport)

    @property
    def custom_report_item(self: "CastSelf") -> "CustomReportItem":
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
class CustomReportItem(_0.APIBase):
    """CustomReportItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_main_report_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMainReportItem")

        if temp is None:
            return False

        return temp

    @is_main_report_item.setter
    @enforce_parameter_types
    def is_main_report_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsMainReportItem",
            bool(value) if value is not None else False,
        )

    @property
    def item_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ItemType")

        if temp is None:
            return ""

        return temp

    def add_condition(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddCondition")

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportItem
        """
        return _Cast_CustomReportItem(self)
