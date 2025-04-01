"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.fluid_film._2372 import (
        AxialFeedJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2373 import (
        AxialGrooveJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2374 import (
        AxialHoleJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2375 import (
        CircumferentialFeedJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2376 import (
        CylindricalHousingJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2377 import (
        MachineryEncasedJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2378 import (
        PadFluidFilmBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2379 import (
        PedestalJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2380 import (
        PlainGreaseFilledJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2381 import (
        PlainGreaseFilledJournalBearingHousingType,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2382 import (
        PlainJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2383 import (
        PlainJournalHousing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2384 import (
        PlainOilFedJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2385 import (
        TiltingPadJournalBearing,
    )
    from mastapy._private.bearings.bearing_designs.fluid_film._2386 import (
        TiltingPadThrustBearing,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.fluid_film._2372": [
            "AxialFeedJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2373": [
            "AxialGrooveJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2374": [
            "AxialHoleJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2375": [
            "CircumferentialFeedJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2376": [
            "CylindricalHousingJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2377": [
            "MachineryEncasedJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2378": ["PadFluidFilmBearing"],
        "_private.bearings.bearing_designs.fluid_film._2379": [
            "PedestalJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2380": [
            "PlainGreaseFilledJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2381": [
            "PlainGreaseFilledJournalBearingHousingType"
        ],
        "_private.bearings.bearing_designs.fluid_film._2382": ["PlainJournalBearing"],
        "_private.bearings.bearing_designs.fluid_film._2383": ["PlainJournalHousing"],
        "_private.bearings.bearing_designs.fluid_film._2384": [
            "PlainOilFedJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2385": [
            "TiltingPadJournalBearing"
        ],
        "_private.bearings.bearing_designs.fluid_film._2386": [
            "TiltingPadThrustBearing"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialFeedJournalBearing",
    "AxialGrooveJournalBearing",
    "AxialHoleJournalBearing",
    "CircumferentialFeedJournalBearing",
    "CylindricalHousingJournalBearing",
    "MachineryEncasedJournalBearing",
    "PadFluidFilmBearing",
    "PedestalJournalBearing",
    "PlainGreaseFilledJournalBearing",
    "PlainGreaseFilledJournalBearingHousingType",
    "PlainJournalBearing",
    "PlainJournalHousing",
    "PlainOilFedJournalBearing",
    "TiltingPadJournalBearing",
    "TiltingPadThrustBearing",
)
