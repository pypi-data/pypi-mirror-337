"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.bevel._1292 import (
        AGMAGleasonConicalGearGeometryMethods,
    )
    from mastapy._private.gears.gear_designs.bevel._1293 import BevelGearDesign
    from mastapy._private.gears.gear_designs.bevel._1294 import BevelGearMeshDesign
    from mastapy._private.gears.gear_designs.bevel._1295 import BevelGearSetDesign
    from mastapy._private.gears.gear_designs.bevel._1296 import BevelMeshedGearDesign
    from mastapy._private.gears.gear_designs.bevel._1297 import (
        DrivenMachineCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1298 import EdgeRadiusType
    from mastapy._private.gears.gear_designs.bevel._1299 import FinishingMethods
    from mastapy._private.gears.gear_designs.bevel._1300 import (
        MachineCharacteristicAGMAKlingelnberg,
    )
    from mastapy._private.gears.gear_designs.bevel._1301 import (
        PrimeMoverCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1302 import (
        ToothProportionsInputMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1303 import (
        ToothThicknessSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1304 import (
        WheelFinishCutterPointWidthRestrictionMethod,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.bevel._1292": [
            "AGMAGleasonConicalGearGeometryMethods"
        ],
        "_private.gears.gear_designs.bevel._1293": ["BevelGearDesign"],
        "_private.gears.gear_designs.bevel._1294": ["BevelGearMeshDesign"],
        "_private.gears.gear_designs.bevel._1295": ["BevelGearSetDesign"],
        "_private.gears.gear_designs.bevel._1296": ["BevelMeshedGearDesign"],
        "_private.gears.gear_designs.bevel._1297": [
            "DrivenMachineCharacteristicGleason"
        ],
        "_private.gears.gear_designs.bevel._1298": ["EdgeRadiusType"],
        "_private.gears.gear_designs.bevel._1299": ["FinishingMethods"],
        "_private.gears.gear_designs.bevel._1300": [
            "MachineCharacteristicAGMAKlingelnberg"
        ],
        "_private.gears.gear_designs.bevel._1301": ["PrimeMoverCharacteristicGleason"],
        "_private.gears.gear_designs.bevel._1302": ["ToothProportionsInputMethod"],
        "_private.gears.gear_designs.bevel._1303": [
            "ToothThicknessSpecificationMethod"
        ],
        "_private.gears.gear_designs.bevel._1304": [
            "WheelFinishCutterPointWidthRestrictionMethod"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearGeometryMethods",
    "BevelGearDesign",
    "BevelGearMeshDesign",
    "BevelGearSetDesign",
    "BevelMeshedGearDesign",
    "DrivenMachineCharacteristicGleason",
    "EdgeRadiusType",
    "FinishingMethods",
    "MachineCharacteristicAGMAKlingelnberg",
    "PrimeMoverCharacteristicGleason",
    "ToothProportionsInputMethod",
    "ToothThicknessSpecificationMethod",
    "WheelFinishCutterPointWidthRestrictionMethod",
)
