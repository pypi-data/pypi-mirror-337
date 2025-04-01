"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.analysis._1328 import AbstractGearAnalysis
    from mastapy._private.gears.analysis._1329 import AbstractGearMeshAnalysis
    from mastapy._private.gears.analysis._1330 import AbstractGearSetAnalysis
    from mastapy._private.gears.analysis._1331 import GearDesignAnalysis
    from mastapy._private.gears.analysis._1332 import GearImplementationAnalysis
    from mastapy._private.gears.analysis._1333 import (
        GearImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1334 import GearImplementationDetail
    from mastapy._private.gears.analysis._1335 import GearMeshDesignAnalysis
    from mastapy._private.gears.analysis._1336 import GearMeshImplementationAnalysis
    from mastapy._private.gears.analysis._1337 import (
        GearMeshImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1338 import GearMeshImplementationDetail
    from mastapy._private.gears.analysis._1339 import GearSetDesignAnalysis
    from mastapy._private.gears.analysis._1340 import GearSetGroupDutyCycle
    from mastapy._private.gears.analysis._1341 import GearSetImplementationAnalysis
    from mastapy._private.gears.analysis._1342 import (
        GearSetImplementationAnalysisAbstract,
    )
    from mastapy._private.gears.analysis._1343 import (
        GearSetImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1344 import GearSetImplementationDetail
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.analysis._1328": ["AbstractGearAnalysis"],
        "_private.gears.analysis._1329": ["AbstractGearMeshAnalysis"],
        "_private.gears.analysis._1330": ["AbstractGearSetAnalysis"],
        "_private.gears.analysis._1331": ["GearDesignAnalysis"],
        "_private.gears.analysis._1332": ["GearImplementationAnalysis"],
        "_private.gears.analysis._1333": ["GearImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1334": ["GearImplementationDetail"],
        "_private.gears.analysis._1335": ["GearMeshDesignAnalysis"],
        "_private.gears.analysis._1336": ["GearMeshImplementationAnalysis"],
        "_private.gears.analysis._1337": ["GearMeshImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1338": ["GearMeshImplementationDetail"],
        "_private.gears.analysis._1339": ["GearSetDesignAnalysis"],
        "_private.gears.analysis._1340": ["GearSetGroupDutyCycle"],
        "_private.gears.analysis._1341": ["GearSetImplementationAnalysis"],
        "_private.gears.analysis._1342": ["GearSetImplementationAnalysisAbstract"],
        "_private.gears.analysis._1343": ["GearSetImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1344": ["GearSetImplementationDetail"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractGearAnalysis",
    "AbstractGearMeshAnalysis",
    "AbstractGearSetAnalysis",
    "GearDesignAnalysis",
    "GearImplementationAnalysis",
    "GearImplementationAnalysisDutyCycle",
    "GearImplementationDetail",
    "GearMeshDesignAnalysis",
    "GearMeshImplementationAnalysis",
    "GearMeshImplementationAnalysisDutyCycle",
    "GearMeshImplementationDetail",
    "GearSetDesignAnalysis",
    "GearSetGroupDutyCycle",
    "GearSetImplementationAnalysis",
    "GearSetImplementationAnalysisAbstract",
    "GearSetImplementationAnalysisDutyCycle",
    "GearSetImplementationDetail",
)
