"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.vectors._2020 import PlaneVectorFieldData
    from mastapy._private.utility.vectors._2021 import PlaneScalarFieldData
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.vectors._2020": ["PlaneVectorFieldData"],
        "_private.utility.vectors._2021": ["PlaneScalarFieldData"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "PlaneVectorFieldData",
    "PlaneScalarFieldData",
)
