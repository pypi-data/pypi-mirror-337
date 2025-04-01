"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2607 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2608 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2609 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2610 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2611 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2612 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2607": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2608": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2609": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2610": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2611": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2612": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
