"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._2038 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._2039 import ConstantLine
    from mastapy._private.utility_gui.charts._2040 import CustomLineChart
    from mastapy._private.utility_gui.charts._2041 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._2042 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._2043 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._2044 import ModeConstantLine
    from mastapy._private.utility_gui.charts._2045 import NDChartDefinition
    from mastapy._private.utility_gui.charts._2046 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._2047 import PointsForSurface
    from mastapy._private.utility_gui.charts._2048 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._2049 import Series2D
    from mastapy._private.utility_gui.charts._2050 import SMTAxis
    from mastapy._private.utility_gui.charts._2051 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._2052 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._2053 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._2038": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._2039": ["ConstantLine"],
        "_private.utility_gui.charts._2040": ["CustomLineChart"],
        "_private.utility_gui.charts._2041": ["CustomTableAndChart"],
        "_private.utility_gui.charts._2042": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._2043": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._2044": ["ModeConstantLine"],
        "_private.utility_gui.charts._2045": ["NDChartDefinition"],
        "_private.utility_gui.charts._2046": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._2047": ["PointsForSurface"],
        "_private.utility_gui.charts._2048": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._2049": ["Series2D"],
        "_private.utility_gui.charts._2050": ["SMTAxis"],
        "_private.utility_gui.charts._2051": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._2052": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._2053": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
