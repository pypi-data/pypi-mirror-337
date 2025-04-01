"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1496 import DynamicForceResults
    from mastapy._private.electric_machines.results._1497 import EfficiencyResults
    from mastapy._private.electric_machines.results._1498 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1499 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1500 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1501 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1502 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1503 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1504 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1505 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1506 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1507 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1508 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1509 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1510 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1511 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1512 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1513 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1515 import LinearDQModel
    from mastapy._private.electric_machines.results._1516 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1517 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1518 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1519 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1520 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1496": ["DynamicForceResults"],
        "_private.electric_machines.results._1497": ["EfficiencyResults"],
        "_private.electric_machines.results._1498": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1499": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1500": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1501": ["ElectricMachineResults"],
        "_private.electric_machines.results._1502": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1503": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1504": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1505": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1506": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1507": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1508": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1509": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1510": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1511": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1512": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1513": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1515": ["LinearDQModel"],
        "_private.electric_machines.results._1516": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1517": ["NonLinearDQModel"],
        "_private.electric_machines.results._1518": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1519": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1520": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
