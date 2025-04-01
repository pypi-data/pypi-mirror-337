"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.face._1086 import FaceGearDesign
    from mastapy._private.gears.gear_designs.face._1087 import (
        FaceGearDiameterFaceWidthSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.face._1088 import FaceGearMeshDesign
    from mastapy._private.gears.gear_designs.face._1089 import FaceGearMeshMicroGeometry
    from mastapy._private.gears.gear_designs.face._1090 import FaceGearMicroGeometry
    from mastapy._private.gears.gear_designs.face._1091 import FaceGearPinionDesign
    from mastapy._private.gears.gear_designs.face._1092 import FaceGearSetDesign
    from mastapy._private.gears.gear_designs.face._1093 import FaceGearSetMicroGeometry
    from mastapy._private.gears.gear_designs.face._1094 import FaceGearWheelDesign
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.face._1086": ["FaceGearDesign"],
        "_private.gears.gear_designs.face._1087": [
            "FaceGearDiameterFaceWidthSpecificationMethod"
        ],
        "_private.gears.gear_designs.face._1088": ["FaceGearMeshDesign"],
        "_private.gears.gear_designs.face._1089": ["FaceGearMeshMicroGeometry"],
        "_private.gears.gear_designs.face._1090": ["FaceGearMicroGeometry"],
        "_private.gears.gear_designs.face._1091": ["FaceGearPinionDesign"],
        "_private.gears.gear_designs.face._1092": ["FaceGearSetDesign"],
        "_private.gears.gear_designs.face._1093": ["FaceGearSetMicroGeometry"],
        "_private.gears.gear_designs.face._1094": ["FaceGearWheelDesign"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FaceGearDesign",
    "FaceGearDiameterFaceWidthSpecificationMethod",
    "FaceGearMeshDesign",
    "FaceGearMeshMicroGeometry",
    "FaceGearMicroGeometry",
    "FaceGearPinionDesign",
    "FaceGearSetDesign",
    "FaceGearSetMicroGeometry",
    "FaceGearWheelDesign",
)
