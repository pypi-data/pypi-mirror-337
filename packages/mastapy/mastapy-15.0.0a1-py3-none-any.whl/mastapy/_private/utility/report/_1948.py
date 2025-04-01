"""CustomReportMultiPropertyItemBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1949

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItemBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2133, _2137, _2145
    from mastapy._private.gears.gear_designs.cylindrical import _1138
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4954,
        _4958,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3057,
    )
    from mastapy._private.utility.report import _1934, _1941, _1947, _1958
    from mastapy._private.utility_gui.charts import _2040, _2041

    Self = TypeVar("Self", bound="CustomReportMultiPropertyItemBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItemBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportMultiPropertyItemBase:
    """Special nested class for casting CustomReportMultiPropertyItemBase to subclasses."""

    __parent__: "CustomReportMultiPropertyItemBase"

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
    def custom_report_chart(self: "CastSelf") -> "_1934.CustomReportChart":
        from mastapy._private.utility.report import _1934

        return self.__parent__._cast(_1934.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1947.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1947

        return self.__parent__._cast(_1947.CustomReportMultiPropertyItem)

    @property
    def custom_table(self: "CastSelf") -> "_1958.CustomTable":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomTable)

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
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "CustomReportMultiPropertyItemBase":
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
class CustomReportMultiPropertyItemBase(_1949.CustomReportNameableItem):
    """CustomReportMultiPropertyItemBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportMultiPropertyItemBase":
        """Cast to another type.

        Returns:
            _Cast_CustomReportMultiPropertyItemBase
        """
        return _Cast_CustomReportMultiPropertyItemBase(self)
