"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1920 import AdHocCustomTable
    from mastapy._private.utility.report._1921 import AxisSettings
    from mastapy._private.utility.report._1922 import BlankRow
    from mastapy._private.utility.report._1923 import CadPageOrientation
    from mastapy._private.utility.report._1924 import CadPageSize
    from mastapy._private.utility.report._1925 import CadTableBorderType
    from mastapy._private.utility.report._1926 import ChartDefinition
    from mastapy._private.utility.report._1927 import SMTChartPointShape
    from mastapy._private.utility.report._1928 import CustomChart
    from mastapy._private.utility.report._1929 import CustomDrawing
    from mastapy._private.utility.report._1930 import CustomGraphic
    from mastapy._private.utility.report._1931 import CustomImage
    from mastapy._private.utility.report._1932 import CustomReport
    from mastapy._private.utility.report._1933 import CustomReportCadDrawing
    from mastapy._private.utility.report._1934 import CustomReportChart
    from mastapy._private.utility.report._1935 import CustomReportChartItem
    from mastapy._private.utility.report._1936 import CustomReportColumn
    from mastapy._private.utility.report._1937 import CustomReportColumns
    from mastapy._private.utility.report._1938 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1939 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1940 import CustomReportHtmlItem
    from mastapy._private.utility.report._1941 import CustomReportItem
    from mastapy._private.utility.report._1942 import CustomReportItemContainer
    from mastapy._private.utility.report._1943 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1944 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1945 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1946 import CustomReportKey
    from mastapy._private.utility.report._1947 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1948 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1949 import CustomReportNameableItem
    from mastapy._private.utility.report._1950 import CustomReportNamedItem
    from mastapy._private.utility.report._1951 import CustomReportPropertyItem
    from mastapy._private.utility.report._1952 import CustomReportStatusItem
    from mastapy._private.utility.report._1953 import CustomReportTab
    from mastapy._private.utility.report._1954 import CustomReportTabs
    from mastapy._private.utility.report._1955 import CustomReportText
    from mastapy._private.utility.report._1956 import CustomRow
    from mastapy._private.utility.report._1957 import CustomSubReport
    from mastapy._private.utility.report._1958 import CustomTable
    from mastapy._private.utility.report._1959 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1960 import DynamicCustomReportItem
    from mastapy._private.utility.report._1961 import FontStyle
    from mastapy._private.utility.report._1962 import FontWeight
    from mastapy._private.utility.report._1963 import HeadingSize
    from mastapy._private.utility.report._1964 import SimpleChartDefinition
    from mastapy._private.utility.report._1965 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1920": ["AdHocCustomTable"],
        "_private.utility.report._1921": ["AxisSettings"],
        "_private.utility.report._1922": ["BlankRow"],
        "_private.utility.report._1923": ["CadPageOrientation"],
        "_private.utility.report._1924": ["CadPageSize"],
        "_private.utility.report._1925": ["CadTableBorderType"],
        "_private.utility.report._1926": ["ChartDefinition"],
        "_private.utility.report._1927": ["SMTChartPointShape"],
        "_private.utility.report._1928": ["CustomChart"],
        "_private.utility.report._1929": ["CustomDrawing"],
        "_private.utility.report._1930": ["CustomGraphic"],
        "_private.utility.report._1931": ["CustomImage"],
        "_private.utility.report._1932": ["CustomReport"],
        "_private.utility.report._1933": ["CustomReportCadDrawing"],
        "_private.utility.report._1934": ["CustomReportChart"],
        "_private.utility.report._1935": ["CustomReportChartItem"],
        "_private.utility.report._1936": ["CustomReportColumn"],
        "_private.utility.report._1937": ["CustomReportColumns"],
        "_private.utility.report._1938": ["CustomReportDefinitionItem"],
        "_private.utility.report._1939": ["CustomReportHorizontalLine"],
        "_private.utility.report._1940": ["CustomReportHtmlItem"],
        "_private.utility.report._1941": ["CustomReportItem"],
        "_private.utility.report._1942": ["CustomReportItemContainer"],
        "_private.utility.report._1943": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1944": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1945": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1946": ["CustomReportKey"],
        "_private.utility.report._1947": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1948": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1949": ["CustomReportNameableItem"],
        "_private.utility.report._1950": ["CustomReportNamedItem"],
        "_private.utility.report._1951": ["CustomReportPropertyItem"],
        "_private.utility.report._1952": ["CustomReportStatusItem"],
        "_private.utility.report._1953": ["CustomReportTab"],
        "_private.utility.report._1954": ["CustomReportTabs"],
        "_private.utility.report._1955": ["CustomReportText"],
        "_private.utility.report._1956": ["CustomRow"],
        "_private.utility.report._1957": ["CustomSubReport"],
        "_private.utility.report._1958": ["CustomTable"],
        "_private.utility.report._1959": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1960": ["DynamicCustomReportItem"],
        "_private.utility.report._1961": ["FontStyle"],
        "_private.utility.report._1962": ["FontWeight"],
        "_private.utility.report._1963": ["HeadingSize"],
        "_private.utility.report._1964": ["SimpleChartDefinition"],
        "_private.utility.report._1965": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
