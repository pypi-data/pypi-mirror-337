"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.straight_bevel_diff._482 import (
        StraightBevelDiffGearMeshRating,
    )
    from mastapy._private.gears.rating.straight_bevel_diff._483 import (
        StraightBevelDiffGearRating,
    )
    from mastapy._private.gears.rating.straight_bevel_diff._484 import (
        StraightBevelDiffGearSetRating,
    )
    from mastapy._private.gears.rating.straight_bevel_diff._485 import (
        StraightBevelDiffMeshedGearRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.straight_bevel_diff._482": [
            "StraightBevelDiffGearMeshRating"
        ],
        "_private.gears.rating.straight_bevel_diff._483": [
            "StraightBevelDiffGearRating"
        ],
        "_private.gears.rating.straight_bevel_diff._484": [
            "StraightBevelDiffGearSetRating"
        ],
        "_private.gears.rating.straight_bevel_diff._485": [
            "StraightBevelDiffMeshedGearRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "StraightBevelDiffGearMeshRating",
    "StraightBevelDiffGearRating",
    "StraightBevelDiffGearSetRating",
    "StraightBevelDiffMeshedGearRating",
)
