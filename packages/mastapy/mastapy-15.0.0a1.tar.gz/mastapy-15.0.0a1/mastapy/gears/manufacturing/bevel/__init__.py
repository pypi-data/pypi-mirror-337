"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.bevel._868 import AbstractTCA
    from mastapy._private.gears.manufacturing.bevel._869 import (
        BevelMachineSettingOptimizationResult,
    )
    from mastapy._private.gears.manufacturing.bevel._870 import (
        ConicalFlankDeviationsData,
    )
    from mastapy._private.gears.manufacturing.bevel._871 import (
        ConicalGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._872 import (
        ConicalGearManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._873 import (
        ConicalGearMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._874 import (
        ConicalGearMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._875 import (
        ConicalMeshedGearManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._876 import (
        ConicalMeshedWheelFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._877 import (
        ConicalMeshFlankManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._878 import (
        ConicalMeshFlankMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._879 import (
        ConicalMeshFlankNURBSMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._880 import (
        ConicalMeshManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._881 import (
        ConicalMeshManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._882 import (
        ConicalMeshMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._883 import (
        ConicalMeshMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._884 import (
        ConicalPinionManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._885 import (
        ConicalPinionMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._886 import (
        ConicalSetManufacturingAnalysis,
    )
    from mastapy._private.gears.manufacturing.bevel._887 import (
        ConicalSetManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._888 import (
        ConicalSetMicroGeometryConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._889 import (
        ConicalSetMicroGeometryConfigBase,
    )
    from mastapy._private.gears.manufacturing.bevel._890 import (
        ConicalWheelManufacturingConfig,
    )
    from mastapy._private.gears.manufacturing.bevel._891 import EaseOffBasedTCA
    from mastapy._private.gears.manufacturing.bevel._892 import FlankMeasurementBorder
    from mastapy._private.gears.manufacturing.bevel._893 import HypoidAdvancedLibrary
    from mastapy._private.gears.manufacturing.bevel._894 import MachineTypes
    from mastapy._private.gears.manufacturing.bevel._895 import ManufacturingMachine
    from mastapy._private.gears.manufacturing.bevel._896 import (
        ManufacturingMachineDatabase,
    )
    from mastapy._private.gears.manufacturing.bevel._897 import (
        PinionBevelGeneratingModifiedRollMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._898 import (
        PinionBevelGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._899 import PinionConcave
    from mastapy._private.gears.manufacturing.bevel._900 import (
        PinionConicalMachineSettingsSpecified,
    )
    from mastapy._private.gears.manufacturing.bevel._901 import PinionConvex
    from mastapy._private.gears.manufacturing.bevel._902 import (
        PinionFinishMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._903 import (
        PinionHypoidFormateTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._904 import (
        PinionHypoidGeneratingTiltMachineSettings,
    )
    from mastapy._private.gears.manufacturing.bevel._905 import PinionMachineSettingsSMT
    from mastapy._private.gears.manufacturing.bevel._906 import (
        PinionRoughMachineSetting,
    )
    from mastapy._private.gears.manufacturing.bevel._907 import Wheel
    from mastapy._private.gears.manufacturing.bevel._908 import WheelFormatMachineTypes
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.bevel._868": ["AbstractTCA"],
        "_private.gears.manufacturing.bevel._869": [
            "BevelMachineSettingOptimizationResult"
        ],
        "_private.gears.manufacturing.bevel._870": ["ConicalFlankDeviationsData"],
        "_private.gears.manufacturing.bevel._871": ["ConicalGearManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._872": ["ConicalGearManufacturingConfig"],
        "_private.gears.manufacturing.bevel._873": ["ConicalGearMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._874": [
            "ConicalGearMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._875": [
            "ConicalMeshedGearManufacturingAnalysis"
        ],
        "_private.gears.manufacturing.bevel._876": [
            "ConicalMeshedWheelFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._877": [
            "ConicalMeshFlankManufacturingConfig"
        ],
        "_private.gears.manufacturing.bevel._878": [
            "ConicalMeshFlankMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._879": [
            "ConicalMeshFlankNURBSMicroGeometryConfig"
        ],
        "_private.gears.manufacturing.bevel._880": ["ConicalMeshManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._881": ["ConicalMeshManufacturingConfig"],
        "_private.gears.manufacturing.bevel._882": ["ConicalMeshMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._883": [
            "ConicalMeshMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._884": ["ConicalPinionManufacturingConfig"],
        "_private.gears.manufacturing.bevel._885": ["ConicalPinionMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._886": ["ConicalSetManufacturingAnalysis"],
        "_private.gears.manufacturing.bevel._887": ["ConicalSetManufacturingConfig"],
        "_private.gears.manufacturing.bevel._888": ["ConicalSetMicroGeometryConfig"],
        "_private.gears.manufacturing.bevel._889": [
            "ConicalSetMicroGeometryConfigBase"
        ],
        "_private.gears.manufacturing.bevel._890": ["ConicalWheelManufacturingConfig"],
        "_private.gears.manufacturing.bevel._891": ["EaseOffBasedTCA"],
        "_private.gears.manufacturing.bevel._892": ["FlankMeasurementBorder"],
        "_private.gears.manufacturing.bevel._893": ["HypoidAdvancedLibrary"],
        "_private.gears.manufacturing.bevel._894": ["MachineTypes"],
        "_private.gears.manufacturing.bevel._895": ["ManufacturingMachine"],
        "_private.gears.manufacturing.bevel._896": ["ManufacturingMachineDatabase"],
        "_private.gears.manufacturing.bevel._897": [
            "PinionBevelGeneratingModifiedRollMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._898": [
            "PinionBevelGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._899": ["PinionConcave"],
        "_private.gears.manufacturing.bevel._900": [
            "PinionConicalMachineSettingsSpecified"
        ],
        "_private.gears.manufacturing.bevel._901": ["PinionConvex"],
        "_private.gears.manufacturing.bevel._902": ["PinionFinishMachineSettings"],
        "_private.gears.manufacturing.bevel._903": [
            "PinionHypoidFormateTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._904": [
            "PinionHypoidGeneratingTiltMachineSettings"
        ],
        "_private.gears.manufacturing.bevel._905": ["PinionMachineSettingsSMT"],
        "_private.gears.manufacturing.bevel._906": ["PinionRoughMachineSetting"],
        "_private.gears.manufacturing.bevel._907": ["Wheel"],
        "_private.gears.manufacturing.bevel._908": ["WheelFormatMachineTypes"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractTCA",
    "BevelMachineSettingOptimizationResult",
    "ConicalFlankDeviationsData",
    "ConicalGearManufacturingAnalysis",
    "ConicalGearManufacturingConfig",
    "ConicalGearMicroGeometryConfig",
    "ConicalGearMicroGeometryConfigBase",
    "ConicalMeshedGearManufacturingAnalysis",
    "ConicalMeshedWheelFlankManufacturingConfig",
    "ConicalMeshFlankManufacturingConfig",
    "ConicalMeshFlankMicroGeometryConfig",
    "ConicalMeshFlankNURBSMicroGeometryConfig",
    "ConicalMeshManufacturingAnalysis",
    "ConicalMeshManufacturingConfig",
    "ConicalMeshMicroGeometryConfig",
    "ConicalMeshMicroGeometryConfigBase",
    "ConicalPinionManufacturingConfig",
    "ConicalPinionMicroGeometryConfig",
    "ConicalSetManufacturingAnalysis",
    "ConicalSetManufacturingConfig",
    "ConicalSetMicroGeometryConfig",
    "ConicalSetMicroGeometryConfigBase",
    "ConicalWheelManufacturingConfig",
    "EaseOffBasedTCA",
    "FlankMeasurementBorder",
    "HypoidAdvancedLibrary",
    "MachineTypes",
    "ManufacturingMachine",
    "ManufacturingMachineDatabase",
    "PinionBevelGeneratingModifiedRollMachineSettings",
    "PinionBevelGeneratingTiltMachineSettings",
    "PinionConcave",
    "PinionConicalMachineSettingsSpecified",
    "PinionConvex",
    "PinionFinishMachineSettings",
    "PinionHypoidFormateTiltMachineSettings",
    "PinionHypoidGeneratingTiltMachineSettings",
    "PinionMachineSettingsSMT",
    "PinionRoughMachineSetting",
    "Wheel",
    "WheelFormatMachineTypes",
)
