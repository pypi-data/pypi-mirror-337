"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.load_case._969 import GearLoadCaseBase
    from mastapy._private.gears.load_case._970 import GearSetLoadCaseBase
    from mastapy._private.gears.load_case._971 import MeshLoadCase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.load_case._969": ["GearLoadCaseBase"],
        "_private.gears.load_case._970": ["GearSetLoadCaseBase"],
        "_private.gears.load_case._971": ["MeshLoadCase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearLoadCaseBase",
    "GearSetLoadCaseBase",
    "MeshLoadCase",
)
