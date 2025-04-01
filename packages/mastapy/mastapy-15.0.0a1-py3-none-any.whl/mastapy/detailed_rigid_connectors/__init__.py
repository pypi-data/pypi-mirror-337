"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors._1563 import (
        DetailedRigidConnectorDesign,
    )
    from mastapy._private.detailed_rigid_connectors._1564 import (
        DetailedRigidConnectorHalfDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors._1563": ["DetailedRigidConnectorDesign"],
        "_private.detailed_rigid_connectors._1564": [
            "DetailedRigidConnectorHalfDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DetailedRigidConnectorDesign",
    "DetailedRigidConnectorHalfDesign",
)
