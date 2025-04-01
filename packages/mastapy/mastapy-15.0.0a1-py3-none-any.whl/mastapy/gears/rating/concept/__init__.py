"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.concept._632 import ConceptGearDutyCycleRating
    from mastapy._private.gears.rating.concept._633 import (
        ConceptGearMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.concept._634 import ConceptGearMeshRating
    from mastapy._private.gears.rating.concept._635 import ConceptGearRating
    from mastapy._private.gears.rating.concept._636 import ConceptGearSetDutyCycleRating
    from mastapy._private.gears.rating.concept._637 import ConceptGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.concept._632": ["ConceptGearDutyCycleRating"],
        "_private.gears.rating.concept._633": ["ConceptGearMeshDutyCycleRating"],
        "_private.gears.rating.concept._634": ["ConceptGearMeshRating"],
        "_private.gears.rating.concept._635": ["ConceptGearRating"],
        "_private.gears.rating.concept._636": ["ConceptGearSetDutyCycleRating"],
        "_private.gears.rating.concept._637": ["ConceptGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConceptGearDutyCycleRating",
    "ConceptGearMeshDutyCycleRating",
    "ConceptGearMeshRating",
    "ConceptGearRating",
    "ConceptGearSetDutyCycleRating",
    "ConceptGearSetRating",
)
