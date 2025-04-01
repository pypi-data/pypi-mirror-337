"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.fe_model.cylindrical._1314 import CylindricalGearFEModel
    from mastapy._private.gears.fe_model.cylindrical._1315 import (
        CylindricalGearMeshFEModel,
    )
    from mastapy._private.gears.fe_model.cylindrical._1316 import (
        CylindricalGearSetFEModel,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.fe_model.cylindrical._1314": ["CylindricalGearFEModel"],
        "_private.gears.fe_model.cylindrical._1315": ["CylindricalGearMeshFEModel"],
        "_private.gears.fe_model.cylindrical._1316": ["CylindricalGearSetFEModel"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearFEModel",
    "CylindricalGearMeshFEModel",
    "CylindricalGearSetFEModel",
)
