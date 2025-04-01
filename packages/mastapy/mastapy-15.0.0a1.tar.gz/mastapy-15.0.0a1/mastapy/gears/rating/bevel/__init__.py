"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.bevel._638 import BevelGearMeshRating
    from mastapy._private.gears.rating.bevel._639 import BevelGearRating
    from mastapy._private.gears.rating.bevel._640 import BevelGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.bevel._638": ["BevelGearMeshRating"],
        "_private.gears.rating.bevel._639": ["BevelGearRating"],
        "_private.gears.rating.bevel._640": ["BevelGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelGearMeshRating",
    "BevelGearRating",
    "BevelGearSetRating",
)
