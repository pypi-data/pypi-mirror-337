"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2831 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2832 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2833 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2834 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2835 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2836 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2837 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2838 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2839 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2840 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2841 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2842 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2843 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2844 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2845 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2846 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2847 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2848 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2849 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2850 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2851 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2852 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2831": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2832": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2833": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2834": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2835": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2836": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2837": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2838": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2839": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2840": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2841": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2842": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2843": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2844": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2845": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2846": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2847": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2848": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2849": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2850": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2851": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2852": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
