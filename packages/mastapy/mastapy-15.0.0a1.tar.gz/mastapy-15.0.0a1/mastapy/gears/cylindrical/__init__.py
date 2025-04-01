"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.cylindrical._1321 import (
        CylindricalGearLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1322 import (
        CylindricalGearLTCAContactCharts,
    )
    from mastapy._private.gears.cylindrical._1323 import (
        CylindricalGearWorstLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1324 import (
        CylindricalGearWorstLTCAContactCharts,
    )
    from mastapy._private.gears.cylindrical._1325 import (
        GearLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1326 import GearLTCAContactCharts
    from mastapy._private.gears.cylindrical._1327 import PointsWithWorstResults
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.cylindrical._1321": [
            "CylindricalGearLTCAContactChartDataAsTextFile"
        ],
        "_private.gears.cylindrical._1322": ["CylindricalGearLTCAContactCharts"],
        "_private.gears.cylindrical._1323": [
            "CylindricalGearWorstLTCAContactChartDataAsTextFile"
        ],
        "_private.gears.cylindrical._1324": ["CylindricalGearWorstLTCAContactCharts"],
        "_private.gears.cylindrical._1325": ["GearLTCAContactChartDataAsTextFile"],
        "_private.gears.cylindrical._1326": ["GearLTCAContactCharts"],
        "_private.gears.cylindrical._1327": ["PointsWithWorstResults"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearLTCAContactChartDataAsTextFile",
    "CylindricalGearLTCAContactCharts",
    "CylindricalGearWorstLTCAContactChartDataAsTextFile",
    "CylindricalGearWorstLTCAContactCharts",
    "GearLTCAContactChartDataAsTextFile",
    "GearLTCAContactCharts",
    "PointsWithWorstResults",
)
