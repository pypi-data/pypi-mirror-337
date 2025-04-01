"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.units_and_measurements._1777 import (
        DegreesMinutesSeconds,
    )
    from mastapy._private.utility.units_and_measurements._1778 import EnumUnit
    from mastapy._private.utility.units_and_measurements._1779 import InverseUnit
    from mastapy._private.utility.units_and_measurements._1780 import MeasurementBase
    from mastapy._private.utility.units_and_measurements._1781 import (
        MeasurementSettings,
    )
    from mastapy._private.utility.units_and_measurements._1782 import MeasurementSystem
    from mastapy._private.utility.units_and_measurements._1783 import SafetyFactorUnit
    from mastapy._private.utility.units_and_measurements._1784 import TimeUnit
    from mastapy._private.utility.units_and_measurements._1785 import Unit
    from mastapy._private.utility.units_and_measurements._1786 import UnitGradient
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.units_and_measurements._1777": ["DegreesMinutesSeconds"],
        "_private.utility.units_and_measurements._1778": ["EnumUnit"],
        "_private.utility.units_and_measurements._1779": ["InverseUnit"],
        "_private.utility.units_and_measurements._1780": ["MeasurementBase"],
        "_private.utility.units_and_measurements._1781": ["MeasurementSettings"],
        "_private.utility.units_and_measurements._1782": ["MeasurementSystem"],
        "_private.utility.units_and_measurements._1783": ["SafetyFactorUnit"],
        "_private.utility.units_and_measurements._1784": ["TimeUnit"],
        "_private.utility.units_and_measurements._1785": ["Unit"],
        "_private.utility.units_and_measurements._1786": ["UnitGradient"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DegreesMinutesSeconds",
    "EnumUnit",
    "InverseUnit",
    "MeasurementBase",
    "MeasurementSettings",
    "MeasurementSystem",
    "SafetyFactorUnit",
    "TimeUnit",
    "Unit",
    "UnitGradient",
)
