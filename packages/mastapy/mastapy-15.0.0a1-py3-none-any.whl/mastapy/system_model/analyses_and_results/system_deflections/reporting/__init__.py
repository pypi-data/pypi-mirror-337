"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3050 import (
        CylindricalGearMeshMisalignmentValue,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3051 import (
        FlexibleGearChart,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3052 import (
        GearInMeshDeflectionResults,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3053 import (
        GearMeshResultsAtOffset,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3054 import (
        PlanetCarrierWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3055 import (
        PlanetPinWindup,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3056 import (
        RigidlyConnectedComponentGroupSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3057 import (
        ShaftSystemDeflectionSectionsReport,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting._3058 import (
        SplineFlankContactReporting,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.system_deflections.reporting._3050": [
            "CylindricalGearMeshMisalignmentValue"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3051": [
            "FlexibleGearChart"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3052": [
            "GearInMeshDeflectionResults"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3053": [
            "GearMeshResultsAtOffset"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3054": [
            "PlanetCarrierWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3055": [
            "PlanetPinWindup"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3056": [
            "RigidlyConnectedComponentGroupSystemDeflection"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3057": [
            "ShaftSystemDeflectionSectionsReport"
        ],
        "_private.system_model.analyses_and_results.system_deflections.reporting._3058": [
            "SplineFlankContactReporting"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshMisalignmentValue",
    "FlexibleGearChart",
    "GearInMeshDeflectionResults",
    "GearMeshResultsAtOffset",
    "PlanetCarrierWindup",
    "PlanetPinWindup",
    "RigidlyConnectedComponentGroupSystemDeflection",
    "ShaftSystemDeflectionSectionsReport",
    "SplineFlankContactReporting",
)
