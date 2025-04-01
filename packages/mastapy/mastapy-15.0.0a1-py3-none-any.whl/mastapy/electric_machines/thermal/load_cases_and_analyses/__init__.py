"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1487 import (
        CoolingLoadCaseSettings,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1488 import (
        HeatDissipationReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1489 import (
        HeatFlowReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1490 import (
        HeatTransferCoefficientReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1491 import (
        PowerLosses,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1492 import (
        PressureDropReporter,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1493 import (
        ThermalAnalysis,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1494 import (
        ThermalLoadCase,
    )
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses._1495 import (
        ThermalLoadCaseGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.load_cases_and_analyses._1487": [
            "CoolingLoadCaseSettings"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1488": [
            "HeatDissipationReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1489": [
            "HeatFlowReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1490": [
            "HeatTransferCoefficientReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1491": [
            "PowerLosses"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1492": [
            "PressureDropReporter"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1493": [
            "ThermalAnalysis"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1494": [
            "ThermalLoadCase"
        ],
        "_private.electric_machines.thermal.load_cases_and_analyses._1495": [
            "ThermalLoadCaseGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CoolingLoadCaseSettings",
    "HeatDissipationReporter",
    "HeatFlowReporter",
    "HeatTransferCoefficientReporter",
    "PowerLosses",
    "PressureDropReporter",
    "ThermalAnalysis",
    "ThermalLoadCase",
    "ThermalLoadCaseGroup",
)
