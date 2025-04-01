"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._574 import (
        MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._575 import (
        PlasticGearVDI2736AbstractGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._576 import (
        PlasticGearVDI2736AbstractMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._577 import (
        PlasticGearVDI2736AbstractRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._578 import (
        PlasticPlasticVDI2736MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._579 import (
        PlasticSNCurveForTheSpecifiedOperatingConditions,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._580 import (
        PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._581 import (
        PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._582 import (
        VDI2736MetalPlasticRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._583 import (
        VDI2736PlasticMetalRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._584 import (
        VDI2736PlasticPlasticRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.plastic_vdi2736._574": [
            "MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._575": [
            "PlasticGearVDI2736AbstractGearSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._576": [
            "PlasticGearVDI2736AbstractMeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._577": [
            "PlasticGearVDI2736AbstractRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._578": [
            "PlasticPlasticVDI2736MeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._579": [
            "PlasticSNCurveForTheSpecifiedOperatingConditions"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._580": [
            "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._581": [
            "PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._582": [
            "VDI2736MetalPlasticRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._583": [
            "VDI2736PlasticMetalRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._584": [
            "VDI2736PlasticPlasticRateableMesh"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating",
    "PlasticGearVDI2736AbstractGearSingleFlankRating",
    "PlasticGearVDI2736AbstractMeshSingleFlankRating",
    "PlasticGearVDI2736AbstractRateableMesh",
    "PlasticPlasticVDI2736MeshSingleFlankRating",
    "PlasticSNCurveForTheSpecifiedOperatingConditions",
    "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",
    "PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh",
    "VDI2736MetalPlasticRateableMesh",
    "VDI2736PlasticMetalRateableMesh",
    "VDI2736PlasticPlasticRateableMesh",
)
