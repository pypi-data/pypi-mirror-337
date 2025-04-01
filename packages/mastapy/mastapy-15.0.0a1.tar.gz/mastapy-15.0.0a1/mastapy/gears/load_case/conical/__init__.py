"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case.conical._981 import ConicalGearLoadCase
    from mastapy._private.gears.load_case.conical._982 import ConicalGearSetLoadCase
    from mastapy._private.gears.load_case.conical._983 import ConicalMeshLoadCase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case.conical._981": ["ConicalGearLoadCase"],
        "_private.gears.load_case.conical._982": ["ConicalGearSetLoadCase"],
        "_private.gears.load_case.conical._983": ["ConicalMeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearLoadCase",
    "ConicalGearSetLoadCase",
    "ConicalMeshLoadCase",
)
