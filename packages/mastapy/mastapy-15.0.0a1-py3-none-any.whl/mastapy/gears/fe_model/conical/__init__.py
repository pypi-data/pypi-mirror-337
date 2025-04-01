"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.fe_model.conical._1317 import ConicalGearFEModel
    from mastapy._private.gears.fe_model.conical._1318 import ConicalMeshFEModel
    from mastapy._private.gears.fe_model.conical._1319 import ConicalSetFEModel
    from mastapy._private.gears.fe_model.conical._1320 import FlankDataSource
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.fe_model.conical._1317": ["ConicalGearFEModel"],
        "_private.gears.fe_model.conical._1318": ["ConicalMeshFEModel"],
        "_private.gears.fe_model.conical._1319": ["ConicalSetFEModel"],
        "_private.gears.fe_model.conical._1320": ["FlankDataSource"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearFEModel",
    "ConicalMeshFEModel",
    "ConicalSetFEModel",
    "FlankDataSource",
)
