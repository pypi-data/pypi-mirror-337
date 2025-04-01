"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.results._1481 import (
        ThermalResultAtLocation,
    )
    from mastapy._private.electric_machines.thermal.results._1482 import ThermalResults
    from mastapy._private.electric_machines.thermal.results._1483 import (
        ThermalResultsForFEComponent,
    )
    from mastapy._private.electric_machines.thermal.results._1484 import (
        ThermalResultsForFERegionOrBoundary,
    )
    from mastapy._private.electric_machines.thermal.results._1485 import (
        ThermalResultsForFESlice,
    )
    from mastapy._private.electric_machines.thermal.results._1486 import (
        ThermalResultsForLPTNNode,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.results._1481": ["ThermalResultAtLocation"],
        "_private.electric_machines.thermal.results._1482": ["ThermalResults"],
        "_private.electric_machines.thermal.results._1483": [
            "ThermalResultsForFEComponent"
        ],
        "_private.electric_machines.thermal.results._1484": [
            "ThermalResultsForFERegionOrBoundary"
        ],
        "_private.electric_machines.thermal.results._1485": [
            "ThermalResultsForFESlice"
        ],
        "_private.electric_machines.thermal.results._1486": [
            "ThermalResultsForLPTNNode"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ThermalResultAtLocation",
    "ThermalResults",
    "ThermalResultsForFEComponent",
    "ThermalResultsForFERegionOrBoundary",
    "ThermalResultsForFESlice",
    "ThermalResultsForLPTNNode",
)
