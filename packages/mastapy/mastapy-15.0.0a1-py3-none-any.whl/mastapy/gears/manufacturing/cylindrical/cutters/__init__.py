"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutters._799 import (
        CurveInLinkedList,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._800 import (
        CustomisableEdgeProfile,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._801 import (
        CylindricalFormedWheelGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._802 import (
        CylindricalGearAbstractCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._803 import (
        CylindricalGearFormGrindingWheel,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._804 import (
        CylindricalGearGrindingWorm,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._805 import (
        CylindricalGearHobDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._806 import (
        CylindricalGearPlungeShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._807 import (
        CylindricalGearPlungeShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._808 import (
        CylindricalGearRackDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._809 import (
        CylindricalGearRealCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._810 import (
        CylindricalGearShaper,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._811 import (
        CylindricalGearShaver,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._812 import (
        CylindricalGearShaverDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._813 import (
        CylindricalWormGrinderDatabase,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._814 import (
        InvoluteCutterDesign,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._815 import (
        MutableCommon,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._816 import (
        MutableCurve,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._817 import (
        MutableFillet,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters._818 import (
        RoughCutterCreationSettings,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutters._799": ["CurveInLinkedList"],
        "_private.gears.manufacturing.cylindrical.cutters._800": [
            "CustomisableEdgeProfile"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._801": [
            "CylindricalFormedWheelGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._802": [
            "CylindricalGearAbstractCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._803": [
            "CylindricalGearFormGrindingWheel"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._804": [
            "CylindricalGearGrindingWorm"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._805": [
            "CylindricalGearHobDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._806": [
            "CylindricalGearPlungeShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._807": [
            "CylindricalGearPlungeShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._808": [
            "CylindricalGearRackDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._809": [
            "CylindricalGearRealCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._810": [
            "CylindricalGearShaper"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._811": [
            "CylindricalGearShaver"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._812": [
            "CylindricalGearShaverDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._813": [
            "CylindricalWormGrinderDatabase"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._814": [
            "InvoluteCutterDesign"
        ],
        "_private.gears.manufacturing.cylindrical.cutters._815": ["MutableCommon"],
        "_private.gears.manufacturing.cylindrical.cutters._816": ["MutableCurve"],
        "_private.gears.manufacturing.cylindrical.cutters._817": ["MutableFillet"],
        "_private.gears.manufacturing.cylindrical.cutters._818": [
            "RoughCutterCreationSettings"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CurveInLinkedList",
    "CustomisableEdgeProfile",
    "CylindricalFormedWheelGrinderDatabase",
    "CylindricalGearAbstractCutterDesign",
    "CylindricalGearFormGrindingWheel",
    "CylindricalGearGrindingWorm",
    "CylindricalGearHobDesign",
    "CylindricalGearPlungeShaver",
    "CylindricalGearPlungeShaverDatabase",
    "CylindricalGearRackDesign",
    "CylindricalGearRealCutterDesign",
    "CylindricalGearShaper",
    "CylindricalGearShaver",
    "CylindricalGearShaverDatabase",
    "CylindricalWormGrinderDatabase",
    "InvoluteCutterDesign",
    "MutableCommon",
    "MutableCurve",
    "MutableFillet",
    "RoughCutterCreationSettings",
)
