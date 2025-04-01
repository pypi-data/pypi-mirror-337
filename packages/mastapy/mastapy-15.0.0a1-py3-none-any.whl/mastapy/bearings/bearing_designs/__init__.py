"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs._2320 import BearingDesign
    from mastapy._private.bearings.bearing_designs._2321 import DetailedBearing
    from mastapy._private.bearings.bearing_designs._2322 import DummyRollingBearing
    from mastapy._private.bearings.bearing_designs._2323 import LinearBearing
    from mastapy._private.bearings.bearing_designs._2324 import NonLinearBearing
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs._2320": ["BearingDesign"],
        "_private.bearings.bearing_designs._2321": ["DetailedBearing"],
        "_private.bearings.bearing_designs._2322": ["DummyRollingBearing"],
        "_private.bearings.bearing_designs._2323": ["LinearBearing"],
        "_private.bearings.bearing_designs._2324": ["NonLinearBearing"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingDesign",
    "DetailedBearing",
    "DummyRollingBearing",
    "LinearBearing",
    "NonLinearBearing",
)
