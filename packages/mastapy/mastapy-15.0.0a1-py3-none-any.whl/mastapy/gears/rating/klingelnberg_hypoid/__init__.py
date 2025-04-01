"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.klingelnberg_hypoid._492 import (
        KlingelnbergCycloPalloidHypoidGearMeshRating,
    )
    from mastapy._private.gears.rating.klingelnberg_hypoid._493 import (
        KlingelnbergCycloPalloidHypoidGearRating,
    )
    from mastapy._private.gears.rating.klingelnberg_hypoid._494 import (
        KlingelnbergCycloPalloidHypoidGearSetRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.klingelnberg_hypoid._492": [
            "KlingelnbergCycloPalloidHypoidGearMeshRating"
        ],
        "_private.gears.rating.klingelnberg_hypoid._493": [
            "KlingelnbergCycloPalloidHypoidGearRating"
        ],
        "_private.gears.rating.klingelnberg_hypoid._494": [
            "KlingelnbergCycloPalloidHypoidGearSetRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergCycloPalloidHypoidGearMeshRating",
    "KlingelnbergCycloPalloidHypoidGearRating",
    "KlingelnbergCycloPalloidHypoidGearSetRating",
)
