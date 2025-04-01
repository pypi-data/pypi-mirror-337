"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials._317 import (
        AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._318 import AcousticRadiationEfficiency
    from mastapy._private.materials._319 import AcousticRadiationEfficiencyInputType
    from mastapy._private.materials._320 import AGMALubricantType
    from mastapy._private.materials._321 import AGMAMaterialApplications
    from mastapy._private.materials._322 import AGMAMaterialClasses
    from mastapy._private.materials._323 import AGMAMaterialGrade
    from mastapy._private.materials._324 import AirProperties
    from mastapy._private.materials._325 import BearingLubricationCondition
    from mastapy._private.materials._326 import BearingMaterial
    from mastapy._private.materials._327 import BearingMaterialDatabase
    from mastapy._private.materials._328 import BHCurveExtrapolationMethod
    from mastapy._private.materials._329 import BHCurveSpecification
    from mastapy._private.materials._330 import ComponentMaterialDatabase
    from mastapy._private.materials._331 import CompositeFatigueSafetyFactorItem
    from mastapy._private.materials._332 import CylindricalGearRatingMethods
    from mastapy._private.materials._333 import DensitySpecificationMethod
    from mastapy._private.materials._334 import FatigueSafetyFactorItem
    from mastapy._private.materials._335 import FatigueSafetyFactorItemBase
    from mastapy._private.materials._336 import Fluid
    from mastapy._private.materials._337 import FluidDatabase
    from mastapy._private.materials._338 import GearingTypes
    from mastapy._private.materials._339 import GeneralTransmissionProperties
    from mastapy._private.materials._340 import GreaseContaminationOptions
    from mastapy._private.materials._341 import HardnessType
    from mastapy._private.materials._342 import ISO76StaticSafetyFactorLimits
    from mastapy._private.materials._343 import ISOLubricantType
    from mastapy._private.materials._344 import LubricantDefinition
    from mastapy._private.materials._345 import LubricantDelivery
    from mastapy._private.materials._346 import LubricantViscosityClassAGMA
    from mastapy._private.materials._347 import LubricantViscosityClassification
    from mastapy._private.materials._348 import LubricantViscosityClassISO
    from mastapy._private.materials._349 import LubricantViscosityClassSAE
    from mastapy._private.materials._350 import LubricationDetail
    from mastapy._private.materials._351 import LubricationDetailDatabase
    from mastapy._private.materials._352 import Material
    from mastapy._private.materials._353 import MaterialDatabase
    from mastapy._private.materials._354 import MaterialsSettings
    from mastapy._private.materials._355 import MaterialsSettingsDatabase
    from mastapy._private.materials._356 import MaterialsSettingsItem
    from mastapy._private.materials._357 import MaterialStandards
    from mastapy._private.materials._358 import MetalPlasticType
    from mastapy._private.materials._359 import OilFiltrationOptions
    from mastapy._private.materials._360 import PressureViscosityCoefficientMethod
    from mastapy._private.materials._361 import QualityGrade
    from mastapy._private.materials._362 import SafetyFactorGroup
    from mastapy._private.materials._363 import SafetyFactorItem
    from mastapy._private.materials._364 import SNCurve
    from mastapy._private.materials._365 import SNCurvePoint
    from mastapy._private.materials._366 import SoundPressureEnclosure
    from mastapy._private.materials._367 import SoundPressureEnclosureType
    from mastapy._private.materials._368 import (
        StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._369 import (
        StressCyclesDataForTheContactSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._370 import TemperatureDependentProperty
    from mastapy._private.materials._371 import TransmissionApplications
    from mastapy._private.materials._372 import VDI2736LubricantType
    from mastapy._private.materials._373 import VehicleDynamicsProperties
    from mastapy._private.materials._374 import WindTurbineStandards
    from mastapy._private.materials._375 import WorkingCharacteristics
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials._317": [
            "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._318": ["AcousticRadiationEfficiency"],
        "_private.materials._319": ["AcousticRadiationEfficiencyInputType"],
        "_private.materials._320": ["AGMALubricantType"],
        "_private.materials._321": ["AGMAMaterialApplications"],
        "_private.materials._322": ["AGMAMaterialClasses"],
        "_private.materials._323": ["AGMAMaterialGrade"],
        "_private.materials._324": ["AirProperties"],
        "_private.materials._325": ["BearingLubricationCondition"],
        "_private.materials._326": ["BearingMaterial"],
        "_private.materials._327": ["BearingMaterialDatabase"],
        "_private.materials._328": ["BHCurveExtrapolationMethod"],
        "_private.materials._329": ["BHCurveSpecification"],
        "_private.materials._330": ["ComponentMaterialDatabase"],
        "_private.materials._331": ["CompositeFatigueSafetyFactorItem"],
        "_private.materials._332": ["CylindricalGearRatingMethods"],
        "_private.materials._333": ["DensitySpecificationMethod"],
        "_private.materials._334": ["FatigueSafetyFactorItem"],
        "_private.materials._335": ["FatigueSafetyFactorItemBase"],
        "_private.materials._336": ["Fluid"],
        "_private.materials._337": ["FluidDatabase"],
        "_private.materials._338": ["GearingTypes"],
        "_private.materials._339": ["GeneralTransmissionProperties"],
        "_private.materials._340": ["GreaseContaminationOptions"],
        "_private.materials._341": ["HardnessType"],
        "_private.materials._342": ["ISO76StaticSafetyFactorLimits"],
        "_private.materials._343": ["ISOLubricantType"],
        "_private.materials._344": ["LubricantDefinition"],
        "_private.materials._345": ["LubricantDelivery"],
        "_private.materials._346": ["LubricantViscosityClassAGMA"],
        "_private.materials._347": ["LubricantViscosityClassification"],
        "_private.materials._348": ["LubricantViscosityClassISO"],
        "_private.materials._349": ["LubricantViscosityClassSAE"],
        "_private.materials._350": ["LubricationDetail"],
        "_private.materials._351": ["LubricationDetailDatabase"],
        "_private.materials._352": ["Material"],
        "_private.materials._353": ["MaterialDatabase"],
        "_private.materials._354": ["MaterialsSettings"],
        "_private.materials._355": ["MaterialsSettingsDatabase"],
        "_private.materials._356": ["MaterialsSettingsItem"],
        "_private.materials._357": ["MaterialStandards"],
        "_private.materials._358": ["MetalPlasticType"],
        "_private.materials._359": ["OilFiltrationOptions"],
        "_private.materials._360": ["PressureViscosityCoefficientMethod"],
        "_private.materials._361": ["QualityGrade"],
        "_private.materials._362": ["SafetyFactorGroup"],
        "_private.materials._363": ["SafetyFactorItem"],
        "_private.materials._364": ["SNCurve"],
        "_private.materials._365": ["SNCurvePoint"],
        "_private.materials._366": ["SoundPressureEnclosure"],
        "_private.materials._367": ["SoundPressureEnclosureType"],
        "_private.materials._368": [
            "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._369": [
            "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._370": ["TemperatureDependentProperty"],
        "_private.materials._371": ["TransmissionApplications"],
        "_private.materials._372": ["VDI2736LubricantType"],
        "_private.materials._373": ["VehicleDynamicsProperties"],
        "_private.materials._374": ["WindTurbineStandards"],
        "_private.materials._375": ["WorkingCharacteristics"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial",
    "AcousticRadiationEfficiency",
    "AcousticRadiationEfficiencyInputType",
    "AGMALubricantType",
    "AGMAMaterialApplications",
    "AGMAMaterialClasses",
    "AGMAMaterialGrade",
    "AirProperties",
    "BearingLubricationCondition",
    "BearingMaterial",
    "BearingMaterialDatabase",
    "BHCurveExtrapolationMethod",
    "BHCurveSpecification",
    "ComponentMaterialDatabase",
    "CompositeFatigueSafetyFactorItem",
    "CylindricalGearRatingMethods",
    "DensitySpecificationMethod",
    "FatigueSafetyFactorItem",
    "FatigueSafetyFactorItemBase",
    "Fluid",
    "FluidDatabase",
    "GearingTypes",
    "GeneralTransmissionProperties",
    "GreaseContaminationOptions",
    "HardnessType",
    "ISO76StaticSafetyFactorLimits",
    "ISOLubricantType",
    "LubricantDefinition",
    "LubricantDelivery",
    "LubricantViscosityClassAGMA",
    "LubricantViscosityClassification",
    "LubricantViscosityClassISO",
    "LubricantViscosityClassSAE",
    "LubricationDetail",
    "LubricationDetailDatabase",
    "Material",
    "MaterialDatabase",
    "MaterialsSettings",
    "MaterialsSettingsDatabase",
    "MaterialsSettingsItem",
    "MaterialStandards",
    "MetalPlasticType",
    "OilFiltrationOptions",
    "PressureViscosityCoefficientMethod",
    "QualityGrade",
    "SafetyFactorGroup",
    "SafetyFactorItem",
    "SNCurve",
    "SNCurvePoint",
    "SoundPressureEnclosure",
    "SoundPressureEnclosureType",
    "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial",
    "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial",
    "TemperatureDependentProperty",
    "TransmissionApplications",
    "VDI2736LubricantType",
    "VehicleDynamicsProperties",
    "WindTurbineStandards",
    "WorkingCharacteristics",
)
