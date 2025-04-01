"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.klingelnberg_conical._495 import (
        KlingelnbergCycloPalloidConicalGearMeshRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical._496 import (
        KlingelnbergCycloPalloidConicalGearRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical._497 import (
        KlingelnbergCycloPalloidConicalGearSetRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.klingelnberg_conical._495": [
            "KlingelnbergCycloPalloidConicalGearMeshRating"
        ],
        "_private.gears.rating.klingelnberg_conical._496": [
            "KlingelnbergCycloPalloidConicalGearRating"
        ],
        "_private.gears.rating.klingelnberg_conical._497": [
            "KlingelnbergCycloPalloidConicalGearSetRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidConicalGearMeshRating",
    "KlingelnbergCycloPalloidConicalGearRating",
    "KlingelnbergCycloPalloidConicalGearSetRating",
)
