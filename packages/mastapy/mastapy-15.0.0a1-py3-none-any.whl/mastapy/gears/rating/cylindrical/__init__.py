"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical._535 import AGMAScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._536 import (
        CylindricalGearDesignAndRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._537 import (
        CylindricalGearDesignAndRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._538 import (
        CylindricalGearDesignAndRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._539 import (
        CylindricalGearDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._540 import (
        CylindricalGearFlankDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._541 import (
        CylindricalGearFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._542 import CylindricalGearMeshRating
    from mastapy._private.gears.rating.cylindrical._543 import (
        CylindricalGearMicroPittingResults,
    )
    from mastapy._private.gears.rating.cylindrical._544 import CylindricalGearRating
    from mastapy._private.gears.rating.cylindrical._545 import (
        CylindricalGearRatingGeometryDataSource,
    )
    from mastapy._private.gears.rating.cylindrical._546 import (
        CylindricalGearScuffingResults,
    )
    from mastapy._private.gears.rating.cylindrical._547 import (
        CylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._548 import CylindricalGearSetRating
    from mastapy._private.gears.rating.cylindrical._549 import (
        CylindricalGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._550 import (
        CylindricalMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._551 import (
        CylindricalMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._552 import (
        CylindricalPlasticGearRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._553 import (
        CylindricalPlasticGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._554 import (
        CylindricalPlasticGearRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._555 import CylindricalRateableMesh
    from mastapy._private.gears.rating.cylindrical._556 import DynamicFactorMethods
    from mastapy._private.gears.rating.cylindrical._557 import (
        GearBlankFactorCalculationOptions,
    )
    from mastapy._private.gears.rating.cylindrical._558 import ISOScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._559 import MeshRatingForReports
    from mastapy._private.gears.rating.cylindrical._560 import MicropittingRatingMethod
    from mastapy._private.gears.rating.cylindrical._561 import MicroPittingResultsRow
    from mastapy._private.gears.rating.cylindrical._562 import (
        MisalignmentContactPatternEnhancements,
    )
    from mastapy._private.gears.rating.cylindrical._563 import RatingMethod
    from mastapy._private.gears.rating.cylindrical._564 import (
        ReducedCylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._565 import (
        ScuffingFlashTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._566 import (
        ScuffingIntegralTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._567 import ScuffingMethods
    from mastapy._private.gears.rating.cylindrical._568 import ScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._569 import ScuffingResultsRowGear
    from mastapy._private.gears.rating.cylindrical._570 import TipReliefScuffingOptions
    from mastapy._private.gears.rating.cylindrical._571 import ToothThicknesses
    from mastapy._private.gears.rating.cylindrical._572 import (
        VDI2737SafetyFactorReportingObject,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical._535": ["AGMAScuffingResultsRow"],
        "_private.gears.rating.cylindrical._536": [
            "CylindricalGearDesignAndRatingSettings"
        ],
        "_private.gears.rating.cylindrical._537": [
            "CylindricalGearDesignAndRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._538": [
            "CylindricalGearDesignAndRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._539": ["CylindricalGearDutyCycleRating"],
        "_private.gears.rating.cylindrical._540": [
            "CylindricalGearFlankDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._541": ["CylindricalGearFlankRating"],
        "_private.gears.rating.cylindrical._542": ["CylindricalGearMeshRating"],
        "_private.gears.rating.cylindrical._543": [
            "CylindricalGearMicroPittingResults"
        ],
        "_private.gears.rating.cylindrical._544": ["CylindricalGearRating"],
        "_private.gears.rating.cylindrical._545": [
            "CylindricalGearRatingGeometryDataSource"
        ],
        "_private.gears.rating.cylindrical._546": ["CylindricalGearScuffingResults"],
        "_private.gears.rating.cylindrical._547": ["CylindricalGearSetDutyCycleRating"],
        "_private.gears.rating.cylindrical._548": ["CylindricalGearSetRating"],
        "_private.gears.rating.cylindrical._549": ["CylindricalGearSingleFlankRating"],
        "_private.gears.rating.cylindrical._550": ["CylindricalMeshDutyCycleRating"],
        "_private.gears.rating.cylindrical._551": ["CylindricalMeshSingleFlankRating"],
        "_private.gears.rating.cylindrical._552": [
            "CylindricalPlasticGearRatingSettings"
        ],
        "_private.gears.rating.cylindrical._553": [
            "CylindricalPlasticGearRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._554": [
            "CylindricalPlasticGearRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._555": ["CylindricalRateableMesh"],
        "_private.gears.rating.cylindrical._556": ["DynamicFactorMethods"],
        "_private.gears.rating.cylindrical._557": ["GearBlankFactorCalculationOptions"],
        "_private.gears.rating.cylindrical._558": ["ISOScuffingResultsRow"],
        "_private.gears.rating.cylindrical._559": ["MeshRatingForReports"],
        "_private.gears.rating.cylindrical._560": ["MicropittingRatingMethod"],
        "_private.gears.rating.cylindrical._561": ["MicroPittingResultsRow"],
        "_private.gears.rating.cylindrical._562": [
            "MisalignmentContactPatternEnhancements"
        ],
        "_private.gears.rating.cylindrical._563": ["RatingMethod"],
        "_private.gears.rating.cylindrical._564": [
            "ReducedCylindricalGearSetDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._565": [
            "ScuffingFlashTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._566": [
            "ScuffingIntegralTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._567": ["ScuffingMethods"],
        "_private.gears.rating.cylindrical._568": ["ScuffingResultsRow"],
        "_private.gears.rating.cylindrical._569": ["ScuffingResultsRowGear"],
        "_private.gears.rating.cylindrical._570": ["TipReliefScuffingOptions"],
        "_private.gears.rating.cylindrical._571": ["ToothThicknesses"],
        "_private.gears.rating.cylindrical._572": [
            "VDI2737SafetyFactorReportingObject"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAScuffingResultsRow",
    "CylindricalGearDesignAndRatingSettings",
    "CylindricalGearDesignAndRatingSettingsDatabase",
    "CylindricalGearDesignAndRatingSettingsItem",
    "CylindricalGearDutyCycleRating",
    "CylindricalGearFlankDutyCycleRating",
    "CylindricalGearFlankRating",
    "CylindricalGearMeshRating",
    "CylindricalGearMicroPittingResults",
    "CylindricalGearRating",
    "CylindricalGearRatingGeometryDataSource",
    "CylindricalGearScuffingResults",
    "CylindricalGearSetDutyCycleRating",
    "CylindricalGearSetRating",
    "CylindricalGearSingleFlankRating",
    "CylindricalMeshDutyCycleRating",
    "CylindricalMeshSingleFlankRating",
    "CylindricalPlasticGearRatingSettings",
    "CylindricalPlasticGearRatingSettingsDatabase",
    "CylindricalPlasticGearRatingSettingsItem",
    "CylindricalRateableMesh",
    "DynamicFactorMethods",
    "GearBlankFactorCalculationOptions",
    "ISOScuffingResultsRow",
    "MeshRatingForReports",
    "MicropittingRatingMethod",
    "MicroPittingResultsRow",
    "MisalignmentContactPatternEnhancements",
    "RatingMethod",
    "ReducedCylindricalGearSetDutyCycleRating",
    "ScuffingFlashTemperatureRatingMethod",
    "ScuffingIntegralTemperatureRatingMethod",
    "ScuffingMethods",
    "ScuffingResultsRow",
    "ScuffingResultsRowGear",
    "TipReliefScuffingOptions",
    "ToothThicknesses",
    "VDI2737SafetyFactorReportingObject",
)
