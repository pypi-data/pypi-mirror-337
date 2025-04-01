"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.elmer._242 import ContactType
    from mastapy._private.nodal_analysis.elmer._243 import ElectricMachineAnalysisPeriod
    from mastapy._private.nodal_analysis.elmer._244 import ElmerResultEntityType
    from mastapy._private.nodal_analysis.elmer._245 import ElmerResults
    from mastapy._private.nodal_analysis.elmer._246 import (
        ElmerResultsFromElectromagneticAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._247 import (
        ElmerResultsFromMechanicalAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._248 import ElmerResultsViewable
    from mastapy._private.nodal_analysis.elmer._249 import ElmerResultType
    from mastapy._private.nodal_analysis.elmer._250 import (
        MechanicalContactSpecification,
    )
    from mastapy._private.nodal_analysis.elmer._251 import MechanicalSolverType
    from mastapy._private.nodal_analysis.elmer._252 import NodalAverageType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.elmer._242": ["ContactType"],
        "_private.nodal_analysis.elmer._243": ["ElectricMachineAnalysisPeriod"],
        "_private.nodal_analysis.elmer._244": ["ElmerResultEntityType"],
        "_private.nodal_analysis.elmer._245": ["ElmerResults"],
        "_private.nodal_analysis.elmer._246": [
            "ElmerResultsFromElectromagneticAnalysis"
        ],
        "_private.nodal_analysis.elmer._247": ["ElmerResultsFromMechanicalAnalysis"],
        "_private.nodal_analysis.elmer._248": ["ElmerResultsViewable"],
        "_private.nodal_analysis.elmer._249": ["ElmerResultType"],
        "_private.nodal_analysis.elmer._250": ["MechanicalContactSpecification"],
        "_private.nodal_analysis.elmer._251": ["MechanicalSolverType"],
        "_private.nodal_analysis.elmer._252": ["NodalAverageType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactType",
    "ElectricMachineAnalysisPeriod",
    "ElmerResultEntityType",
    "ElmerResults",
    "ElmerResultsFromElectromagneticAnalysis",
    "ElmerResultsFromMechanicalAnalysis",
    "ElmerResultsViewable",
    "ElmerResultType",
    "MechanicalContactSpecification",
    "MechanicalSolverType",
    "NodalAverageType",
)
