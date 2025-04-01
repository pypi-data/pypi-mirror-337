"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.virtual_cylindrical_gears._462 import (
        BevelVirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._463 import (
        BevelVirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._464 import (
        BevelVirtualCylindricalGearSetISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._465 import (
        HypoidVirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._466 import (
        HypoidVirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._467 import (
        HypoidVirtualCylindricalGearSetISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._468 import (
        KlingelnbergHypoidVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._469 import (
        KlingelnbergSpiralBevelVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._470 import (
        KlingelnbergVirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._471 import (
        KlingelnbergVirtualCylindricalGearSet,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._472 import (
        VirtualCylindricalGear,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._473 import (
        VirtualCylindricalGearBasic,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._474 import (
        VirtualCylindricalGearISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._475 import (
        VirtualCylindricalGearISO10300MethodB2,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._476 import (
        VirtualCylindricalGearSet,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._477 import (
        VirtualCylindricalGearSetISO10300MethodB1,
    )
    from mastapy._private.gears.rating.virtual_cylindrical_gears._478 import (
        VirtualCylindricalGearSetISO10300MethodB2,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.virtual_cylindrical_gears._462": [
            "BevelVirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._463": [
            "BevelVirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._464": [
            "BevelVirtualCylindricalGearSetISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._465": [
            "HypoidVirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._466": [
            "HypoidVirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._467": [
            "HypoidVirtualCylindricalGearSetISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._468": [
            "KlingelnbergHypoidVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._469": [
            "KlingelnbergSpiralBevelVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._470": [
            "KlingelnbergVirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._471": [
            "KlingelnbergVirtualCylindricalGearSet"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._472": [
            "VirtualCylindricalGear"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._473": [
            "VirtualCylindricalGearBasic"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._474": [
            "VirtualCylindricalGearISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._475": [
            "VirtualCylindricalGearISO10300MethodB2"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._476": [
            "VirtualCylindricalGearSet"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._477": [
            "VirtualCylindricalGearSetISO10300MethodB1"
        ],
        "_private.gears.rating.virtual_cylindrical_gears._478": [
            "VirtualCylindricalGearSetISO10300MethodB2"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BevelVirtualCylindricalGearISO10300MethodB2",
    "BevelVirtualCylindricalGearSetISO10300MethodB1",
    "BevelVirtualCylindricalGearSetISO10300MethodB2",
    "HypoidVirtualCylindricalGearISO10300MethodB2",
    "HypoidVirtualCylindricalGearSetISO10300MethodB1",
    "HypoidVirtualCylindricalGearSetISO10300MethodB2",
    "KlingelnbergHypoidVirtualCylindricalGear",
    "KlingelnbergSpiralBevelVirtualCylindricalGear",
    "KlingelnbergVirtualCylindricalGear",
    "KlingelnbergVirtualCylindricalGearSet",
    "VirtualCylindricalGear",
    "VirtualCylindricalGearBasic",
    "VirtualCylindricalGearISO10300MethodB1",
    "VirtualCylindricalGearISO10300MethodB2",
    "VirtualCylindricalGearSet",
    "VirtualCylindricalGearSetISO10300MethodB1",
    "VirtualCylindricalGearSetISO10300MethodB2",
)
