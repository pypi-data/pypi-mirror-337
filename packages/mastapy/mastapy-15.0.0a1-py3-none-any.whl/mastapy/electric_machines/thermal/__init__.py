"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal._1453 import (
        AdditionalSliceSpecification,
    )
    from mastapy._private.electric_machines.thermal._1454 import Channel
    from mastapy._private.electric_machines.thermal._1455 import ComponentSetup
    from mastapy._private.electric_machines.thermal._1456 import CoolingJacketType
    from mastapy._private.electric_machines.thermal._1457 import (
        CutoutsForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1458 import (
        EndWindingCoolingFlowSource,
    )
    from mastapy._private.electric_machines.thermal._1459 import EndWindingLengthSource
    from mastapy._private.electric_machines.thermal._1460 import (
        EndWindingThermalElement,
    )
    from mastapy._private.electric_machines.thermal._1461 import (
        HousingChannelModificationFactors,
    )
    from mastapy._private.electric_machines.thermal._1462 import HousingFlowDirection
    from mastapy._private.electric_machines.thermal._1463 import InitialInformation
    from mastapy._private.electric_machines.thermal._1464 import InletLocation
    from mastapy._private.electric_machines.thermal._1465 import (
        RegionIDForThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal._1466 import RotorSetup
    from mastapy._private.electric_machines.thermal._1467 import SliceLengthInformation
    from mastapy._private.electric_machines.thermal._1468 import (
        SliceLengthInformationPerRegion,
    )
    from mastapy._private.electric_machines.thermal._1469 import (
        SliceLengthInformationReporter,
    )
    from mastapy._private.electric_machines.thermal._1470 import StatorSetup
    from mastapy._private.electric_machines.thermal._1471 import ThermalElectricMachine
    from mastapy._private.electric_machines.thermal._1472 import (
        ThermalElectricMachineSetup,
    )
    from mastapy._private.electric_machines.thermal._1473 import ThermalEndcap
    from mastapy._private.electric_machines.thermal._1474 import ThermalEndWinding
    from mastapy._private.electric_machines.thermal._1475 import (
        ThermalEndWindingSurfaceCollection,
    )
    from mastapy._private.electric_machines.thermal._1476 import ThermalHousing
    from mastapy._private.electric_machines.thermal._1477 import ThermalRotor
    from mastapy._private.electric_machines.thermal._1478 import ThermalStator
    from mastapy._private.electric_machines.thermal._1479 import ThermalWindings
    from mastapy._private.electric_machines.thermal._1480 import (
        UserSpecifiedEdgeIndices,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal._1453": ["AdditionalSliceSpecification"],
        "_private.electric_machines.thermal._1454": ["Channel"],
        "_private.electric_machines.thermal._1455": ["ComponentSetup"],
        "_private.electric_machines.thermal._1456": ["CoolingJacketType"],
        "_private.electric_machines.thermal._1457": ["CutoutsForThermalAnalysis"],
        "_private.electric_machines.thermal._1458": ["EndWindingCoolingFlowSource"],
        "_private.electric_machines.thermal._1459": ["EndWindingLengthSource"],
        "_private.electric_machines.thermal._1460": ["EndWindingThermalElement"],
        "_private.electric_machines.thermal._1461": [
            "HousingChannelModificationFactors"
        ],
        "_private.electric_machines.thermal._1462": ["HousingFlowDirection"],
        "_private.electric_machines.thermal._1463": ["InitialInformation"],
        "_private.electric_machines.thermal._1464": ["InletLocation"],
        "_private.electric_machines.thermal._1465": ["RegionIDForThermalAnalysis"],
        "_private.electric_machines.thermal._1466": ["RotorSetup"],
        "_private.electric_machines.thermal._1467": ["SliceLengthInformation"],
        "_private.electric_machines.thermal._1468": ["SliceLengthInformationPerRegion"],
        "_private.electric_machines.thermal._1469": ["SliceLengthInformationReporter"],
        "_private.electric_machines.thermal._1470": ["StatorSetup"],
        "_private.electric_machines.thermal._1471": ["ThermalElectricMachine"],
        "_private.electric_machines.thermal._1472": ["ThermalElectricMachineSetup"],
        "_private.electric_machines.thermal._1473": ["ThermalEndcap"],
        "_private.electric_machines.thermal._1474": ["ThermalEndWinding"],
        "_private.electric_machines.thermal._1475": [
            "ThermalEndWindingSurfaceCollection"
        ],
        "_private.electric_machines.thermal._1476": ["ThermalHousing"],
        "_private.electric_machines.thermal._1477": ["ThermalRotor"],
        "_private.electric_machines.thermal._1478": ["ThermalStator"],
        "_private.electric_machines.thermal._1479": ["ThermalWindings"],
        "_private.electric_machines.thermal._1480": ["UserSpecifiedEdgeIndices"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdditionalSliceSpecification",
    "Channel",
    "ComponentSetup",
    "CoolingJacketType",
    "CutoutsForThermalAnalysis",
    "EndWindingCoolingFlowSource",
    "EndWindingLengthSource",
    "EndWindingThermalElement",
    "HousingChannelModificationFactors",
    "HousingFlowDirection",
    "InitialInformation",
    "InletLocation",
    "RegionIDForThermalAnalysis",
    "RotorSetup",
    "SliceLengthInformation",
    "SliceLengthInformationPerRegion",
    "SliceLengthInformationReporter",
    "StatorSetup",
    "ThermalElectricMachine",
    "ThermalElectricMachineSetup",
    "ThermalEndcap",
    "ThermalEndWinding",
    "ThermalEndWindingSurfaceCollection",
    "ThermalHousing",
    "ThermalRotor",
    "ThermalStator",
    "ThermalWindings",
    "UserSpecifiedEdgeIndices",
)
