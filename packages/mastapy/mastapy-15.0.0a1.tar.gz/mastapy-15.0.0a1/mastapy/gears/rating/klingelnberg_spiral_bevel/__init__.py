"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel._489 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshRating,
    )
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel._490 import (
        KlingelnbergCycloPalloidSpiralBevelGearRating,
    )
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel._491 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.klingelnberg_spiral_bevel._489": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshRating"
        ],
        "_private.gears.rating.klingelnberg_spiral_bevel._490": [
            "KlingelnbergCycloPalloidSpiralBevelGearRating"
        ],
        "_private.gears.rating.klingelnberg_spiral_bevel._491": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidSpiralBevelGearMeshRating",
    "KlingelnbergCycloPalloidSpiralBevelGearRating",
    "KlingelnbergCycloPalloidSpiralBevelGearSetRating",
)
