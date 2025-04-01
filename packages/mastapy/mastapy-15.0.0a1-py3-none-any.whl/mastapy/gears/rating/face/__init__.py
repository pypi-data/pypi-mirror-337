"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.face._529 import FaceGearDutyCycleRating
    from mastapy._private.gears.rating.face._530 import FaceGearMeshDutyCycleRating
    from mastapy._private.gears.rating.face._531 import FaceGearMeshRating
    from mastapy._private.gears.rating.face._532 import FaceGearRating
    from mastapy._private.gears.rating.face._533 import FaceGearSetDutyCycleRating
    from mastapy._private.gears.rating.face._534 import FaceGearSetRating
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.face._529": ["FaceGearDutyCycleRating"],
        "_private.gears.rating.face._530": ["FaceGearMeshDutyCycleRating"],
        "_private.gears.rating.face._531": ["FaceGearMeshRating"],
        "_private.gears.rating.face._532": ["FaceGearRating"],
        "_private.gears.rating.face._533": ["FaceGearSetDutyCycleRating"],
        "_private.gears.rating.face._534": ["FaceGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDutyCycleRating",
    "FaceGearMeshDutyCycleRating",
    "FaceGearMeshRating",
    "FaceGearRating",
    "FaceGearSetDutyCycleRating",
    "FaceGearSetRating",
)
