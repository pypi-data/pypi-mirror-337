"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs._1037 import (
        BevelHypoidGearDesignSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._1038 import (
        BevelHypoidGearDesignSettingsItem,
    )
    from mastapy._private.gears.gear_designs._1039 import (
        BevelHypoidGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.gear_designs._1040 import (
        BevelHypoidGearRatingSettingsItem,
    )
    from mastapy._private.gears.gear_designs._1041 import DesignConstraint
    from mastapy._private.gears.gear_designs._1042 import (
        DesignConstraintCollectionDatabase,
    )
    from mastapy._private.gears.gear_designs._1043 import DesignConstraintsCollection
    from mastapy._private.gears.gear_designs._1044 import GearDesign
    from mastapy._private.gears.gear_designs._1045 import GearDesignComponent
    from mastapy._private.gears.gear_designs._1046 import GearMeshDesign
    from mastapy._private.gears.gear_designs._1047 import GearSetDesign
    from mastapy._private.gears.gear_designs._1048 import (
        SelectedDesignConstraintsCollection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs._1037": ["BevelHypoidGearDesignSettingsDatabase"],
        "_private.gears.gear_designs._1038": ["BevelHypoidGearDesignSettingsItem"],
        "_private.gears.gear_designs._1039": ["BevelHypoidGearRatingSettingsDatabase"],
        "_private.gears.gear_designs._1040": ["BevelHypoidGearRatingSettingsItem"],
        "_private.gears.gear_designs._1041": ["DesignConstraint"],
        "_private.gears.gear_designs._1042": ["DesignConstraintCollectionDatabase"],
        "_private.gears.gear_designs._1043": ["DesignConstraintsCollection"],
        "_private.gears.gear_designs._1044": ["GearDesign"],
        "_private.gears.gear_designs._1045": ["GearDesignComponent"],
        "_private.gears.gear_designs._1046": ["GearMeshDesign"],
        "_private.gears.gear_designs._1047": ["GearSetDesign"],
        "_private.gears.gear_designs._1048": ["SelectedDesignConstraintsCollection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelHypoidGearDesignSettingsDatabase",
    "BevelHypoidGearDesignSettingsItem",
    "BevelHypoidGearRatingSettingsDatabase",
    "BevelHypoidGearRatingSettingsItem",
    "DesignConstraint",
    "DesignConstraintCollectionDatabase",
    "DesignConstraintsCollection",
    "GearDesign",
    "GearDesignComponent",
    "GearMeshDesign",
    "GearSetDesign",
    "SelectedDesignConstraintsCollection",
)
