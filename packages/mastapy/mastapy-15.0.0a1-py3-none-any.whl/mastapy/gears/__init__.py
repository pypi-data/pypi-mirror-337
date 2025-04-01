"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears._397 import AccuracyGrades
    from mastapy._private.gears._398 import AGMAToleranceStandard
    from mastapy._private.gears._399 import BevelHypoidGearDesignSettings
    from mastapy._private.gears._400 import BevelHypoidGearRatingSettings
    from mastapy._private.gears._401 import CentreDistanceChangeMethod
    from mastapy._private.gears._402 import CoefficientOfFrictionCalculationMethod
    from mastapy._private.gears._403 import ConicalGearToothSurface
    from mastapy._private.gears._404 import ContactRatioDataSource
    from mastapy._private.gears._405 import ContactRatioRequirements
    from mastapy._private.gears._406 import CylindricalFlanks
    from mastapy._private.gears._407 import CylindricalMisalignmentDataSource
    from mastapy._private.gears._408 import DeflectionFromBendingOption
    from mastapy._private.gears._409 import GearFlanks
    from mastapy._private.gears._410 import GearNURBSSurface
    from mastapy._private.gears._411 import GearSetDesignGroup
    from mastapy._private.gears._412 import GearSetModes
    from mastapy._private.gears._413 import GearSetOptimisationResult
    from mastapy._private.gears._414 import GearSetOptimisationResults
    from mastapy._private.gears._415 import GearSetOptimiser
    from mastapy._private.gears._416 import Hand
    from mastapy._private.gears._417 import ISOToleranceStandard
    from mastapy._private.gears._418 import LubricationMethods
    from mastapy._private.gears._419 import MicroGeometryInputTypes
    from mastapy._private.gears._420 import MicroGeometryModel
    from mastapy._private.gears._421 import (
        MicropittingCoefficientOfFrictionCalculationMethod,
    )
    from mastapy._private.gears._422 import NamedPlanetAngle
    from mastapy._private.gears._423 import PlanetaryDetail
    from mastapy._private.gears._424 import PlanetaryRatingLoadSharingOption
    from mastapy._private.gears._425 import PocketingPowerLossCoefficients
    from mastapy._private.gears._426 import PocketingPowerLossCoefficientsDatabase
    from mastapy._private.gears._427 import QualityGradeTypes
    from mastapy._private.gears._428 import SafetyRequirementsAGMA
    from mastapy._private.gears._429 import (
        SpecificationForTheEffectOfOilKinematicViscosity,
    )
    from mastapy._private.gears._430 import SpiralBevelRootLineTilt
    from mastapy._private.gears._431 import SpiralBevelToothTaper
    from mastapy._private.gears._432 import TESpecificationType
    from mastapy._private.gears._433 import WormAddendumFactor
    from mastapy._private.gears._434 import WormType
    from mastapy._private.gears._435 import ZerolBevelGleasonToothTaperOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears._397": ["AccuracyGrades"],
        "_private.gears._398": ["AGMAToleranceStandard"],
        "_private.gears._399": ["BevelHypoidGearDesignSettings"],
        "_private.gears._400": ["BevelHypoidGearRatingSettings"],
        "_private.gears._401": ["CentreDistanceChangeMethod"],
        "_private.gears._402": ["CoefficientOfFrictionCalculationMethod"],
        "_private.gears._403": ["ConicalGearToothSurface"],
        "_private.gears._404": ["ContactRatioDataSource"],
        "_private.gears._405": ["ContactRatioRequirements"],
        "_private.gears._406": ["CylindricalFlanks"],
        "_private.gears._407": ["CylindricalMisalignmentDataSource"],
        "_private.gears._408": ["DeflectionFromBendingOption"],
        "_private.gears._409": ["GearFlanks"],
        "_private.gears._410": ["GearNURBSSurface"],
        "_private.gears._411": ["GearSetDesignGroup"],
        "_private.gears._412": ["GearSetModes"],
        "_private.gears._413": ["GearSetOptimisationResult"],
        "_private.gears._414": ["GearSetOptimisationResults"],
        "_private.gears._415": ["GearSetOptimiser"],
        "_private.gears._416": ["Hand"],
        "_private.gears._417": ["ISOToleranceStandard"],
        "_private.gears._418": ["LubricationMethods"],
        "_private.gears._419": ["MicroGeometryInputTypes"],
        "_private.gears._420": ["MicroGeometryModel"],
        "_private.gears._421": ["MicropittingCoefficientOfFrictionCalculationMethod"],
        "_private.gears._422": ["NamedPlanetAngle"],
        "_private.gears._423": ["PlanetaryDetail"],
        "_private.gears._424": ["PlanetaryRatingLoadSharingOption"],
        "_private.gears._425": ["PocketingPowerLossCoefficients"],
        "_private.gears._426": ["PocketingPowerLossCoefficientsDatabase"],
        "_private.gears._427": ["QualityGradeTypes"],
        "_private.gears._428": ["SafetyRequirementsAGMA"],
        "_private.gears._429": ["SpecificationForTheEffectOfOilKinematicViscosity"],
        "_private.gears._430": ["SpiralBevelRootLineTilt"],
        "_private.gears._431": ["SpiralBevelToothTaper"],
        "_private.gears._432": ["TESpecificationType"],
        "_private.gears._433": ["WormAddendumFactor"],
        "_private.gears._434": ["WormType"],
        "_private.gears._435": ["ZerolBevelGleasonToothTaperOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AccuracyGrades",
    "AGMAToleranceStandard",
    "BevelHypoidGearDesignSettings",
    "BevelHypoidGearRatingSettings",
    "CentreDistanceChangeMethod",
    "CoefficientOfFrictionCalculationMethod",
    "ConicalGearToothSurface",
    "ContactRatioDataSource",
    "ContactRatioRequirements",
    "CylindricalFlanks",
    "CylindricalMisalignmentDataSource",
    "DeflectionFromBendingOption",
    "GearFlanks",
    "GearNURBSSurface",
    "GearSetDesignGroup",
    "GearSetModes",
    "GearSetOptimisationResult",
    "GearSetOptimisationResults",
    "GearSetOptimiser",
    "Hand",
    "ISOToleranceStandard",
    "LubricationMethods",
    "MicroGeometryInputTypes",
    "MicroGeometryModel",
    "MicropittingCoefficientOfFrictionCalculationMethod",
    "NamedPlanetAngle",
    "PlanetaryDetail",
    "PlanetaryRatingLoadSharingOption",
    "PocketingPowerLossCoefficients",
    "PocketingPowerLossCoefficientsDatabase",
    "QualityGradeTypes",
    "SafetyRequirementsAGMA",
    "SpecificationForTheEffectOfOilKinematicViscosity",
    "SpiralBevelRootLineTilt",
    "SpiralBevelToothTaper",
    "TESpecificationType",
    "WormAddendumFactor",
    "WormType",
    "ZerolBevelGleasonToothTaperOption",
)
