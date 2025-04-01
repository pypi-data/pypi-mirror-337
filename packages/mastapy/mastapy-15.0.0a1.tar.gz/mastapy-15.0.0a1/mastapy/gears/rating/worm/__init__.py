"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.worm._456 import WormGearDutyCycleRating
    from mastapy._private.gears.rating.worm._457 import WormGearMeshRating
    from mastapy._private.gears.rating.worm._458 import WormGearRating
    from mastapy._private.gears.rating.worm._459 import WormGearSetDutyCycleRating
    from mastapy._private.gears.rating.worm._460 import WormGearSetRating
    from mastapy._private.gears.rating.worm._461 import WormMeshDutyCycleRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.worm._456": ["WormGearDutyCycleRating"],
        "_private.gears.rating.worm._457": ["WormGearMeshRating"],
        "_private.gears.rating.worm._458": ["WormGearRating"],
        "_private.gears.rating.worm._459": ["WormGearSetDutyCycleRating"],
        "_private.gears.rating.worm._460": ["WormGearSetRating"],
        "_private.gears.rating.worm._461": ["WormMeshDutyCycleRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "WormGearDutyCycleRating",
    "WormGearMeshRating",
    "WormGearRating",
    "WormGearSetDutyCycleRating",
    "WormGearSetRating",
    "WormMeshDutyCycleRating",
)
