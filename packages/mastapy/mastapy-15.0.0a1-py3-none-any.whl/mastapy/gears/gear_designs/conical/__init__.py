"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.conical._1263 import ActiveConicalFlank
    from mastapy._private.gears.gear_designs.conical._1264 import (
        BacklashDistributionRule,
    )
    from mastapy._private.gears.gear_designs.conical._1265 import ConicalFlanks
    from mastapy._private.gears.gear_designs.conical._1266 import ConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1267 import ConicalGearDesign
    from mastapy._private.gears.gear_designs.conical._1268 import ConicalGearMeshDesign
    from mastapy._private.gears.gear_designs.conical._1269 import ConicalGearSetDesign
    from mastapy._private.gears.gear_designs.conical._1270 import (
        ConicalMachineSettingCalculationMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1271 import (
        ConicalManufactureMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1272 import (
        ConicalMeshedGearDesign,
    )
    from mastapy._private.gears.gear_designs.conical._1273 import (
        ConicalMeshMisalignments,
    )
    from mastapy._private.gears.gear_designs.conical._1274 import CutterBladeType
    from mastapy._private.gears.gear_designs.conical._1275 import CutterGaugeLengths
    from mastapy._private.gears.gear_designs.conical._1276 import DummyConicalGearCutter
    from mastapy._private.gears.gear_designs.conical._1277 import FrontEndTypes
    from mastapy._private.gears.gear_designs.conical._1278 import (
        GleasonSafetyRequirements,
    )
    from mastapy._private.gears.gear_designs.conical._1279 import (
        KIMoSBevelHypoidSingleLoadCaseResultsData,
    )
    from mastapy._private.gears.gear_designs.conical._1280 import (
        KIMoSBevelHypoidSingleRotationAngleResult,
    )
    from mastapy._private.gears.gear_designs.conical._1281 import (
        KlingelnbergFinishingMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1282 import (
        LoadDistributionFactorMethods,
    )
    from mastapy._private.gears.gear_designs.conical._1283 import TopremEntryType
    from mastapy._private.gears.gear_designs.conical._1284 import TopremLetter
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.conical._1263": ["ActiveConicalFlank"],
        "_private.gears.gear_designs.conical._1264": ["BacklashDistributionRule"],
        "_private.gears.gear_designs.conical._1265": ["ConicalFlanks"],
        "_private.gears.gear_designs.conical._1266": ["ConicalGearCutter"],
        "_private.gears.gear_designs.conical._1267": ["ConicalGearDesign"],
        "_private.gears.gear_designs.conical._1268": ["ConicalGearMeshDesign"],
        "_private.gears.gear_designs.conical._1269": ["ConicalGearSetDesign"],
        "_private.gears.gear_designs.conical._1270": [
            "ConicalMachineSettingCalculationMethods"
        ],
        "_private.gears.gear_designs.conical._1271": ["ConicalManufactureMethods"],
        "_private.gears.gear_designs.conical._1272": ["ConicalMeshedGearDesign"],
        "_private.gears.gear_designs.conical._1273": ["ConicalMeshMisalignments"],
        "_private.gears.gear_designs.conical._1274": ["CutterBladeType"],
        "_private.gears.gear_designs.conical._1275": ["CutterGaugeLengths"],
        "_private.gears.gear_designs.conical._1276": ["DummyConicalGearCutter"],
        "_private.gears.gear_designs.conical._1277": ["FrontEndTypes"],
        "_private.gears.gear_designs.conical._1278": ["GleasonSafetyRequirements"],
        "_private.gears.gear_designs.conical._1279": [
            "KIMoSBevelHypoidSingleLoadCaseResultsData"
        ],
        "_private.gears.gear_designs.conical._1280": [
            "KIMoSBevelHypoidSingleRotationAngleResult"
        ],
        "_private.gears.gear_designs.conical._1281": ["KlingelnbergFinishingMethods"],
        "_private.gears.gear_designs.conical._1282": ["LoadDistributionFactorMethods"],
        "_private.gears.gear_designs.conical._1283": ["TopremEntryType"],
        "_private.gears.gear_designs.conical._1284": ["TopremLetter"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveConicalFlank",
    "BacklashDistributionRule",
    "ConicalFlanks",
    "ConicalGearCutter",
    "ConicalGearDesign",
    "ConicalGearMeshDesign",
    "ConicalGearSetDesign",
    "ConicalMachineSettingCalculationMethods",
    "ConicalManufactureMethods",
    "ConicalMeshedGearDesign",
    "ConicalMeshMisalignments",
    "CutterBladeType",
    "CutterGaugeLengths",
    "DummyConicalGearCutter",
    "FrontEndTypes",
    "GleasonSafetyRequirements",
    "KIMoSBevelHypoidSingleLoadCaseResultsData",
    "KIMoSBevelHypoidSingleRotationAngleResult",
    "KlingelnbergFinishingMethods",
    "LoadDistributionFactorMethods",
    "TopremEntryType",
    "TopremLetter",
)
