"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.materials._667 import AGMACylindricalGearMaterial
    from mastapy._private.gears.materials._668 import (
        BenedictAndKelleyCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._669 import BevelGearAbstractMaterialDatabase
    from mastapy._private.gears.materials._670 import BevelGearISOMaterial
    from mastapy._private.gears.materials._671 import BevelGearISOMaterialDatabase
    from mastapy._private.gears.materials._672 import BevelGearMaterial
    from mastapy._private.gears.materials._673 import BevelGearMaterialDatabase
    from mastapy._private.gears.materials._674 import CoefficientOfFrictionCalculator
    from mastapy._private.gears.materials._675 import (
        CylindricalGearAGMAMaterialDatabase,
    )
    from mastapy._private.gears.materials._676 import CylindricalGearISOMaterialDatabase
    from mastapy._private.gears.materials._677 import CylindricalGearMaterial
    from mastapy._private.gears.materials._678 import CylindricalGearMaterialDatabase
    from mastapy._private.gears.materials._679 import (
        CylindricalGearPlasticMaterialDatabase,
    )
    from mastapy._private.gears.materials._680 import (
        DrozdovAndGavrikovCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._681 import GearMaterial
    from mastapy._private.gears.materials._682 import GearMaterialDatabase
    from mastapy._private.gears.materials._683 import (
        GearMaterialExpertSystemFactorSettings,
    )
    from mastapy._private.gears.materials._684 import (
        InstantaneousCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._685 import (
        ISO14179Part1CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._686 import (
        ISO14179Part2CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._687 import (
        ISO14179Part2CoefficientOfFrictionCalculatorBase,
    )
    from mastapy._private.gears.materials._688 import (
        ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification,
    )
    from mastapy._private.gears.materials._689 import ISOCylindricalGearMaterial
    from mastapy._private.gears.materials._690 import (
        ISOTC60CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._691 import (
        ISOTR1417912001CoefficientOfFrictionConstants,
    )
    from mastapy._private.gears.materials._692 import (
        ISOTR1417912001CoefficientOfFrictionConstantsDatabase,
    )
    from mastapy._private.gears.materials._693 import (
        KlingelnbergConicalGearMaterialDatabase,
    )
    from mastapy._private.gears.materials._694 import (
        KlingelnbergCycloPalloidConicalGearMaterial,
    )
    from mastapy._private.gears.materials._695 import ManufactureRating
    from mastapy._private.gears.materials._696 import (
        MisharinCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._697 import (
        ODonoghueAndCameronCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._698 import PlasticCylindricalGearMaterial
    from mastapy._private.gears.materials._699 import PlasticSNCurve
    from mastapy._private.gears.materials._700 import RatingMethods
    from mastapy._private.gears.materials._701 import RawMaterial
    from mastapy._private.gears.materials._702 import RawMaterialDatabase
    from mastapy._private.gears.materials._703 import (
        ScriptCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._704 import SNCurveDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.materials._667": ["AGMACylindricalGearMaterial"],
        "_private.gears.materials._668": [
            "BenedictAndKelleyCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._669": ["BevelGearAbstractMaterialDatabase"],
        "_private.gears.materials._670": ["BevelGearISOMaterial"],
        "_private.gears.materials._671": ["BevelGearISOMaterialDatabase"],
        "_private.gears.materials._672": ["BevelGearMaterial"],
        "_private.gears.materials._673": ["BevelGearMaterialDatabase"],
        "_private.gears.materials._674": ["CoefficientOfFrictionCalculator"],
        "_private.gears.materials._675": ["CylindricalGearAGMAMaterialDatabase"],
        "_private.gears.materials._676": ["CylindricalGearISOMaterialDatabase"],
        "_private.gears.materials._677": ["CylindricalGearMaterial"],
        "_private.gears.materials._678": ["CylindricalGearMaterialDatabase"],
        "_private.gears.materials._679": ["CylindricalGearPlasticMaterialDatabase"],
        "_private.gears.materials._680": [
            "DrozdovAndGavrikovCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._681": ["GearMaterial"],
        "_private.gears.materials._682": ["GearMaterialDatabase"],
        "_private.gears.materials._683": ["GearMaterialExpertSystemFactorSettings"],
        "_private.gears.materials._684": [
            "InstantaneousCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._685": [
            "ISO14179Part1CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._686": [
            "ISO14179Part2CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._687": [
            "ISO14179Part2CoefficientOfFrictionCalculatorBase"
        ],
        "_private.gears.materials._688": [
            "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification"
        ],
        "_private.gears.materials._689": ["ISOCylindricalGearMaterial"],
        "_private.gears.materials._690": ["ISOTC60CoefficientOfFrictionCalculator"],
        "_private.gears.materials._691": [
            "ISOTR1417912001CoefficientOfFrictionConstants"
        ],
        "_private.gears.materials._692": [
            "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        ],
        "_private.gears.materials._693": ["KlingelnbergConicalGearMaterialDatabase"],
        "_private.gears.materials._694": [
            "KlingelnbergCycloPalloidConicalGearMaterial"
        ],
        "_private.gears.materials._695": ["ManufactureRating"],
        "_private.gears.materials._696": ["MisharinCoefficientOfFrictionCalculator"],
        "_private.gears.materials._697": [
            "ODonoghueAndCameronCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._698": ["PlasticCylindricalGearMaterial"],
        "_private.gears.materials._699": ["PlasticSNCurve"],
        "_private.gears.materials._700": ["RatingMethods"],
        "_private.gears.materials._701": ["RawMaterial"],
        "_private.gears.materials._702": ["RawMaterialDatabase"],
        "_private.gears.materials._703": ["ScriptCoefficientOfFrictionCalculator"],
        "_private.gears.materials._704": ["SNCurveDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMACylindricalGearMaterial",
    "BenedictAndKelleyCoefficientOfFrictionCalculator",
    "BevelGearAbstractMaterialDatabase",
    "BevelGearISOMaterial",
    "BevelGearISOMaterialDatabase",
    "BevelGearMaterial",
    "BevelGearMaterialDatabase",
    "CoefficientOfFrictionCalculator",
    "CylindricalGearAGMAMaterialDatabase",
    "CylindricalGearISOMaterialDatabase",
    "CylindricalGearMaterial",
    "CylindricalGearMaterialDatabase",
    "CylindricalGearPlasticMaterialDatabase",
    "DrozdovAndGavrikovCoefficientOfFrictionCalculator",
    "GearMaterial",
    "GearMaterialDatabase",
    "GearMaterialExpertSystemFactorSettings",
    "InstantaneousCoefficientOfFrictionCalculator",
    "ISO14179Part1CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculatorBase",
    "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification",
    "ISOCylindricalGearMaterial",
    "ISOTC60CoefficientOfFrictionCalculator",
    "ISOTR1417912001CoefficientOfFrictionConstants",
    "ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
    "KlingelnbergConicalGearMaterialDatabase",
    "KlingelnbergCycloPalloidConicalGearMaterial",
    "ManufactureRating",
    "MisharinCoefficientOfFrictionCalculator",
    "ODonoghueAndCameronCoefficientOfFrictionCalculator",
    "PlasticCylindricalGearMaterial",
    "PlasticSNCurve",
    "RatingMethods",
    "RawMaterial",
    "RawMaterialDatabase",
    "ScriptCoefficientOfFrictionCalculator",
    "SNCurveDefinition",
)
