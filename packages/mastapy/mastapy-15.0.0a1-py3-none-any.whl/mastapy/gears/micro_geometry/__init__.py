"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.micro_geometry._653 import BiasModification
    from mastapy._private.gears.micro_geometry._654 import FlankMicroGeometry
    from mastapy._private.gears.micro_geometry._655 import FlankSide
    from mastapy._private.gears.micro_geometry._656 import LeadModification
    from mastapy._private.gears.micro_geometry._657 import (
        LocationOfEvaluationLowerLimit,
    )
    from mastapy._private.gears.micro_geometry._658 import (
        LocationOfEvaluationUpperLimit,
    )
    from mastapy._private.gears.micro_geometry._659 import (
        LocationOfRootReliefEvaluation,
    )
    from mastapy._private.gears.micro_geometry._660 import LocationOfTipReliefEvaluation
    from mastapy._private.gears.micro_geometry._661 import (
        MainProfileReliefEndsAtTheStartOfRootReliefOption,
    )
    from mastapy._private.gears.micro_geometry._662 import (
        MainProfileReliefEndsAtTheStartOfTipReliefOption,
    )
    from mastapy._private.gears.micro_geometry._663 import Modification
    from mastapy._private.gears.micro_geometry._664 import (
        ParabolicRootReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._665 import (
        ParabolicTipReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._666 import ProfileModification
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.micro_geometry._653": ["BiasModification"],
        "_private.gears.micro_geometry._654": ["FlankMicroGeometry"],
        "_private.gears.micro_geometry._655": ["FlankSide"],
        "_private.gears.micro_geometry._656": ["LeadModification"],
        "_private.gears.micro_geometry._657": ["LocationOfEvaluationLowerLimit"],
        "_private.gears.micro_geometry._658": ["LocationOfEvaluationUpperLimit"],
        "_private.gears.micro_geometry._659": ["LocationOfRootReliefEvaluation"],
        "_private.gears.micro_geometry._660": ["LocationOfTipReliefEvaluation"],
        "_private.gears.micro_geometry._661": [
            "MainProfileReliefEndsAtTheStartOfRootReliefOption"
        ],
        "_private.gears.micro_geometry._662": [
            "MainProfileReliefEndsAtTheStartOfTipReliefOption"
        ],
        "_private.gears.micro_geometry._663": ["Modification"],
        "_private.gears.micro_geometry._664": [
            "ParabolicRootReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._665": [
            "ParabolicTipReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._666": ["ProfileModification"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BiasModification",
    "FlankMicroGeometry",
    "FlankSide",
    "LeadModification",
    "LocationOfEvaluationLowerLimit",
    "LocationOfEvaluationUpperLimit",
    "LocationOfRootReliefEvaluation",
    "LocationOfTipReliefEvaluation",
    "MainProfileReliefEndsAtTheStartOfRootReliefOption",
    "MainProfileReliefEndsAtTheStartOfTipReliefOption",
    "Modification",
    "ParabolicRootReliefStartsTangentToMainProfileRelief",
    "ParabolicTipReliefStartsTangentToMainProfileRelief",
    "ProfileModification",
)
