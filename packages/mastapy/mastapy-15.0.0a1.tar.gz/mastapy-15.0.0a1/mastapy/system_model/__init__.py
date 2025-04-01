"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2391 import Design
    from mastapy._private.system_model._2392 import ComponentDampingOption
    from mastapy._private.system_model._2393 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2394 import DesignEntity
    from mastapy._private.system_model._2395 import DesignEntityId
    from mastapy._private.system_model._2396 import DesignSettings
    from mastapy._private.system_model._2397 import DutyCycleImporter
    from mastapy._private.system_model._2398 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2399 import ExternalFullFELoader
    from mastapy._private.system_model._2400 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2401 import IncludeDutyCycleOption
    from mastapy._private.system_model._2402 import MAAElectricMachineGroup
    from mastapy._private.system_model._2403 import MASTASettings
    from mastapy._private.system_model._2404 import MemorySummary
    from mastapy._private.system_model._2405 import MeshStiffnessModel
    from mastapy._private.system_model._2406 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2407 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2408 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2409 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2410 import PowerLoadType
    from mastapy._private.system_model._2411 import RelativeComponentAlignment
    from mastapy._private.system_model._2412 import RelativeOffsetOption
    from mastapy._private.system_model._2413 import SystemReporting
    from mastapy._private.system_model._2414 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2415 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2391": ["Design"],
        "_private.system_model._2392": ["ComponentDampingOption"],
        "_private.system_model._2393": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2394": ["DesignEntity"],
        "_private.system_model._2395": ["DesignEntityId"],
        "_private.system_model._2396": ["DesignSettings"],
        "_private.system_model._2397": ["DutyCycleImporter"],
        "_private.system_model._2398": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2399": ["ExternalFullFELoader"],
        "_private.system_model._2400": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2401": ["IncludeDutyCycleOption"],
        "_private.system_model._2402": ["MAAElectricMachineGroup"],
        "_private.system_model._2403": ["MASTASettings"],
        "_private.system_model._2404": ["MemorySummary"],
        "_private.system_model._2405": ["MeshStiffnessModel"],
        "_private.system_model._2406": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2407": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2408": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2409": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2410": ["PowerLoadType"],
        "_private.system_model._2411": ["RelativeComponentAlignment"],
        "_private.system_model._2412": ["RelativeOffsetOption"],
        "_private.system_model._2413": ["SystemReporting"],
        "_private.system_model._2414": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2415": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
