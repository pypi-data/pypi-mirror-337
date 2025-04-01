"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.enums._1999 import BearingForceArrowOption
    from mastapy._private.utility.enums._2000 import PropertySpecificationMethod
    from mastapy._private.utility.enums._2001 import TableAndChartOptions
    from mastapy._private.utility.enums._2002 import ThreeDViewContourOption
    from mastapy._private.utility.enums._2003 import (
        ThreeDViewContourOptionFirstSelection,
    )
    from mastapy._private.utility.enums._2004 import (
        ThreeDViewContourOptionSecondSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.enums._1999": ["BearingForceArrowOption"],
        "_private.utility.enums._2000": ["PropertySpecificationMethod"],
        "_private.utility.enums._2001": ["TableAndChartOptions"],
        "_private.utility.enums._2002": ["ThreeDViewContourOption"],
        "_private.utility.enums._2003": ["ThreeDViewContourOptionFirstSelection"],
        "_private.utility.enums._2004": ["ThreeDViewContourOptionSecondSelection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingForceArrowOption",
    "PropertySpecificationMethod",
    "TableAndChartOptions",
    "ThreeDViewContourOption",
    "ThreeDViewContourOptionFirstSelection",
    "ThreeDViewContourOptionSecondSelection",
)
