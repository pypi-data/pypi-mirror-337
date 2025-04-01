"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.conical._959 import ConicalGearBendingStiffness
    from mastapy._private.gears.ltca.conical._960 import ConicalGearBendingStiffnessNode
    from mastapy._private.gears.ltca.conical._961 import ConicalGearContactStiffness
    from mastapy._private.gears.ltca.conical._962 import ConicalGearContactStiffnessNode
    from mastapy._private.gears.ltca.conical._963 import (
        ConicalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._964 import (
        ConicalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._965 import (
        ConicalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._966 import (
        ConicalMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.conical._967 import (
        ConicalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.conical._968 import ConicalMeshLoadedContactLine
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.conical._959": ["ConicalGearBendingStiffness"],
        "_private.gears.ltca.conical._960": ["ConicalGearBendingStiffnessNode"],
        "_private.gears.ltca.conical._961": ["ConicalGearContactStiffness"],
        "_private.gears.ltca.conical._962": ["ConicalGearContactStiffnessNode"],
        "_private.gears.ltca.conical._963": ["ConicalGearLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._964": ["ConicalGearSetLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._965": [
            "ConicalMeshedGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.conical._966": ["ConicalMeshLoadDistributionAnalysis"],
        "_private.gears.ltca.conical._967": ["ConicalMeshLoadDistributionAtRotation"],
        "_private.gears.ltca.conical._968": ["ConicalMeshLoadedContactLine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearBendingStiffness",
    "ConicalGearBendingStiffnessNode",
    "ConicalGearContactStiffness",
    "ConicalGearContactStiffnessNode",
    "ConicalGearLoadDistributionAnalysis",
    "ConicalGearSetLoadDistributionAnalysis",
    "ConicalMeshedGearLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAnalysis",
    "ConicalMeshLoadDistributionAtRotation",
    "ConicalMeshLoadedContactLine",
)
