"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2417 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2418 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2419 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2420 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2421 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2422 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2423 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2424 import OptimizationStep
    from mastapy._private.system_model.optimization._2425 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2426 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2427 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2417": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2418": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2419": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2420": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2421": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2422": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2423": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2424": ["OptimizationStep"],
        "_private.system_model.optimization._2425": ["OptimizationStrategy"],
        "_private.system_model.optimization._2426": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2427": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
