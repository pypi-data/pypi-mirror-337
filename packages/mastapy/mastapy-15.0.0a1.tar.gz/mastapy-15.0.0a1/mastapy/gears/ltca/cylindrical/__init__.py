"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca.cylindrical._947 import (
        CylindricalGearBendingStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._948 import (
        CylindricalGearBendingStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._949 import (
        CylindricalGearContactStiffness,
    )
    from mastapy._private.gears.ltca.cylindrical._950 import (
        CylindricalGearContactStiffnessNode,
    )
    from mastapy._private.gears.ltca.cylindrical._951 import CylindricalGearFESettings
    from mastapy._private.gears.ltca.cylindrical._952 import (
        CylindricalGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._953 import (
        CylindricalGearMeshLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._954 import (
        CylindricalGearMeshLoadedContactLine,
    )
    from mastapy._private.gears.ltca.cylindrical._955 import (
        CylindricalGearMeshLoadedContactPoint,
    )
    from mastapy._private.gears.ltca.cylindrical._956 import (
        CylindricalGearSetLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca.cylindrical._957 import (
        CylindricalMeshLoadDistributionAtRotation,
    )
    from mastapy._private.gears.ltca.cylindrical._958 import (
        FaceGearSetLoadDistributionAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca.cylindrical._947": ["CylindricalGearBendingStiffness"],
        "_private.gears.ltca.cylindrical._948": ["CylindricalGearBendingStiffnessNode"],
        "_private.gears.ltca.cylindrical._949": ["CylindricalGearContactStiffness"],
        "_private.gears.ltca.cylindrical._950": ["CylindricalGearContactStiffnessNode"],
        "_private.gears.ltca.cylindrical._951": ["CylindricalGearFESettings"],
        "_private.gears.ltca.cylindrical._952": [
            "CylindricalGearLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._953": [
            "CylindricalGearMeshLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._954": [
            "CylindricalGearMeshLoadedContactLine"
        ],
        "_private.gears.ltca.cylindrical._955": [
            "CylindricalGearMeshLoadedContactPoint"
        ],
        "_private.gears.ltca.cylindrical._956": [
            "CylindricalGearSetLoadDistributionAnalysis"
        ],
        "_private.gears.ltca.cylindrical._957": [
            "CylindricalMeshLoadDistributionAtRotation"
        ],
        "_private.gears.ltca.cylindrical._958": ["FaceGearSetLoadDistributionAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBendingStiffness",
    "CylindricalGearBendingStiffnessNode",
    "CylindricalGearContactStiffness",
    "CylindricalGearContactStiffnessNode",
    "CylindricalGearFESettings",
    "CylindricalGearLoadDistributionAnalysis",
    "CylindricalGearMeshLoadDistributionAnalysis",
    "CylindricalGearMeshLoadedContactLine",
    "CylindricalGearMeshLoadedContactPoint",
    "CylindricalGearSetLoadDistributionAnalysis",
    "CylindricalMeshLoadDistributionAtRotation",
    "FaceGearSetLoadDistributionAnalysis",
)
