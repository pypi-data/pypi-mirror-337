"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_two_d_fe_analysis._990 import (
        CylindricalGearMeshTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._991 import (
        CylindricalGearMeshTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._992 import (
        CylindricalGearSetTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._993 import (
        CylindricalGearSetTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._994 import (
        CylindricalGearTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._995 import (
        CylindricalGearTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._996 import (
        CylindricalGearTwoDimensionalFEAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._997 import (
        FindleyCriticalPlaneAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_two_d_fe_analysis._990": [
            "CylindricalGearMeshTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._991": [
            "CylindricalGearMeshTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._992": [
            "CylindricalGearSetTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._993": [
            "CylindricalGearSetTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._994": ["CylindricalGearTIFFAnalysis"],
        "_private.gears.gear_two_d_fe_analysis._995": [
            "CylindricalGearTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._996": [
            "CylindricalGearTwoDimensionalFEAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._997": ["FindleyCriticalPlaneAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshTIFFAnalysis",
    "CylindricalGearMeshTIFFAnalysisDutyCycle",
    "CylindricalGearSetTIFFAnalysis",
    "CylindricalGearSetTIFFAnalysisDutyCycle",
    "CylindricalGearTIFFAnalysis",
    "CylindricalGearTIFFAnalysisDutyCycle",
    "CylindricalGearTwoDimensionalFEAnalysis",
    "FindleyCriticalPlaneAnalysis",
)
