"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials.efficiency._376 import BearingEfficiencyRatingMethod
    from mastapy._private.materials.efficiency._377 import CombinedResistiveTorque
    from mastapy._private.materials.efficiency._378 import IndependentPowerLoss
    from mastapy._private.materials.efficiency._379 import IndependentResistiveTorque
    from mastapy._private.materials.efficiency._380 import LoadAndSpeedCombinedPowerLoss
    from mastapy._private.materials.efficiency._381 import OilPumpDetail
    from mastapy._private.materials.efficiency._382 import OilPumpDriveType
    from mastapy._private.materials.efficiency._383 import OilSealLossCalculationMethod
    from mastapy._private.materials.efficiency._384 import OilSealMaterialType
    from mastapy._private.materials.efficiency._385 import PowerLoss
    from mastapy._private.materials.efficiency._386 import ResistiveTorque
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials.efficiency._376": ["BearingEfficiencyRatingMethod"],
        "_private.materials.efficiency._377": ["CombinedResistiveTorque"],
        "_private.materials.efficiency._378": ["IndependentPowerLoss"],
        "_private.materials.efficiency._379": ["IndependentResistiveTorque"],
        "_private.materials.efficiency._380": ["LoadAndSpeedCombinedPowerLoss"],
        "_private.materials.efficiency._381": ["OilPumpDetail"],
        "_private.materials.efficiency._382": ["OilPumpDriveType"],
        "_private.materials.efficiency._383": ["OilSealLossCalculationMethod"],
        "_private.materials.efficiency._384": ["OilSealMaterialType"],
        "_private.materials.efficiency._385": ["PowerLoss"],
        "_private.materials.efficiency._386": ["ResistiveTorque"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingEfficiencyRatingMethod",
    "CombinedResistiveTorque",
    "IndependentPowerLoss",
    "IndependentResistiveTorque",
    "LoadAndSpeedCombinedPowerLoss",
    "OilPumpDetail",
    "OilPumpDriveType",
    "OilSealLossCalculationMethod",
    "OilSealMaterialType",
    "PowerLoss",
    "ResistiveTorque",
)
