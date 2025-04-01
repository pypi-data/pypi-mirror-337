"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.ltca._921 import ConicalGearFilletStressResults
    from mastapy._private.gears.ltca._922 import ConicalGearRootFilletStressResults
    from mastapy._private.gears.ltca._923 import ContactResultType
    from mastapy._private.gears.ltca._924 import CylindricalGearFilletNodeStressResults
    from mastapy._private.gears.ltca._925 import (
        CylindricalGearFilletNodeStressResultsColumn,
    )
    from mastapy._private.gears.ltca._926 import (
        CylindricalGearFilletNodeStressResultsRow,
    )
    from mastapy._private.gears.ltca._927 import CylindricalGearRootFilletStressResults
    from mastapy._private.gears.ltca._928 import (
        CylindricalMeshedGearLoadDistributionAnalysis,
    )
    from mastapy._private.gears.ltca._929 import GearBendingStiffness
    from mastapy._private.gears.ltca._930 import GearBendingStiffnessNode
    from mastapy._private.gears.ltca._931 import GearContactStiffness
    from mastapy._private.gears.ltca._932 import GearContactStiffnessNode
    from mastapy._private.gears.ltca._933 import GearFilletNodeStressResults
    from mastapy._private.gears.ltca._934 import GearFilletNodeStressResultsColumn
    from mastapy._private.gears.ltca._935 import GearFilletNodeStressResultsRow
    from mastapy._private.gears.ltca._936 import GearLoadDistributionAnalysis
    from mastapy._private.gears.ltca._937 import GearMeshLoadDistributionAnalysis
    from mastapy._private.gears.ltca._938 import GearMeshLoadDistributionAtRotation
    from mastapy._private.gears.ltca._939 import GearMeshLoadedContactLine
    from mastapy._private.gears.ltca._940 import GearMeshLoadedContactPoint
    from mastapy._private.gears.ltca._941 import GearRootFilletStressResults
    from mastapy._private.gears.ltca._942 import GearSetLoadDistributionAnalysis
    from mastapy._private.gears.ltca._943 import GearStiffness
    from mastapy._private.gears.ltca._944 import GearStiffnessNode
    from mastapy._private.gears.ltca._945 import (
        MeshedGearLoadDistributionAnalysisAtRotation,
    )
    from mastapy._private.gears.ltca._946 import UseAdvancedLTCAOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.ltca._921": ["ConicalGearFilletStressResults"],
        "_private.gears.ltca._922": ["ConicalGearRootFilletStressResults"],
        "_private.gears.ltca._923": ["ContactResultType"],
        "_private.gears.ltca._924": ["CylindricalGearFilletNodeStressResults"],
        "_private.gears.ltca._925": ["CylindricalGearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._926": ["CylindricalGearFilletNodeStressResultsRow"],
        "_private.gears.ltca._927": ["CylindricalGearRootFilletStressResults"],
        "_private.gears.ltca._928": ["CylindricalMeshedGearLoadDistributionAnalysis"],
        "_private.gears.ltca._929": ["GearBendingStiffness"],
        "_private.gears.ltca._930": ["GearBendingStiffnessNode"],
        "_private.gears.ltca._931": ["GearContactStiffness"],
        "_private.gears.ltca._932": ["GearContactStiffnessNode"],
        "_private.gears.ltca._933": ["GearFilletNodeStressResults"],
        "_private.gears.ltca._934": ["GearFilletNodeStressResultsColumn"],
        "_private.gears.ltca._935": ["GearFilletNodeStressResultsRow"],
        "_private.gears.ltca._936": ["GearLoadDistributionAnalysis"],
        "_private.gears.ltca._937": ["GearMeshLoadDistributionAnalysis"],
        "_private.gears.ltca._938": ["GearMeshLoadDistributionAtRotation"],
        "_private.gears.ltca._939": ["GearMeshLoadedContactLine"],
        "_private.gears.ltca._940": ["GearMeshLoadedContactPoint"],
        "_private.gears.ltca._941": ["GearRootFilletStressResults"],
        "_private.gears.ltca._942": ["GearSetLoadDistributionAnalysis"],
        "_private.gears.ltca._943": ["GearStiffness"],
        "_private.gears.ltca._944": ["GearStiffnessNode"],
        "_private.gears.ltca._945": ["MeshedGearLoadDistributionAnalysisAtRotation"],
        "_private.gears.ltca._946": ["UseAdvancedLTCAOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearFilletStressResults",
    "ConicalGearRootFilletStressResults",
    "ContactResultType",
    "CylindricalGearFilletNodeStressResults",
    "CylindricalGearFilletNodeStressResultsColumn",
    "CylindricalGearFilletNodeStressResultsRow",
    "CylindricalGearRootFilletStressResults",
    "CylindricalMeshedGearLoadDistributionAnalysis",
    "GearBendingStiffness",
    "GearBendingStiffnessNode",
    "GearContactStiffness",
    "GearContactStiffnessNode",
    "GearFilletNodeStressResults",
    "GearFilletNodeStressResultsColumn",
    "GearFilletNodeStressResultsRow",
    "GearLoadDistributionAnalysis",
    "GearMeshLoadDistributionAnalysis",
    "GearMeshLoadDistributionAtRotation",
    "GearMeshLoadedContactLine",
    "GearMeshLoadedContactPoint",
    "GearRootFilletStressResults",
    "GearSetLoadDistributionAnalysis",
    "GearStiffness",
    "GearStiffnessNode",
    "MeshedGearLoadDistributionAnalysisAtRotation",
    "UseAdvancedLTCAOptions",
)
