"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.roller_bearing_profiles._2113 import ProfileDataToUse
    from mastapy._private.bearings.roller_bearing_profiles._2114 import ProfileSet
    from mastapy._private.bearings.roller_bearing_profiles._2115 import ProfileToFit
    from mastapy._private.bearings.roller_bearing_profiles._2116 import (
        RollerBearingConicalProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2117 import (
        RollerBearingCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2118 import (
        RollerBearingDinLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2119 import (
        RollerBearingFlatProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2120 import (
        RollerBearingJohnsGoharProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2121 import (
        RollerBearingLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2122 import (
        RollerBearingProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2123 import (
        RollerBearingTangentialCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2124 import (
        RollerBearingUserSpecifiedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2125 import (
        RollerRaceProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2126 import (
        UserSpecifiedProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2127 import (
        UserSpecifiedRollerRaceProfilePoint,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.roller_bearing_profiles._2113": ["ProfileDataToUse"],
        "_private.bearings.roller_bearing_profiles._2114": ["ProfileSet"],
        "_private.bearings.roller_bearing_profiles._2115": ["ProfileToFit"],
        "_private.bearings.roller_bearing_profiles._2116": [
            "RollerBearingConicalProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2117": [
            "RollerBearingCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2118": [
            "RollerBearingDinLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2119": ["RollerBearingFlatProfile"],
        "_private.bearings.roller_bearing_profiles._2120": [
            "RollerBearingJohnsGoharProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2121": [
            "RollerBearingLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2122": ["RollerBearingProfile"],
        "_private.bearings.roller_bearing_profiles._2123": [
            "RollerBearingTangentialCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2124": [
            "RollerBearingUserSpecifiedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2125": ["RollerRaceProfilePoint"],
        "_private.bearings.roller_bearing_profiles._2126": [
            "UserSpecifiedProfilePoint"
        ],
        "_private.bearings.roller_bearing_profiles._2127": [
            "UserSpecifiedRollerRaceProfilePoint"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ProfileDataToUse",
    "ProfileSet",
    "ProfileToFit",
    "RollerBearingConicalProfile",
    "RollerBearingCrownedProfile",
    "RollerBearingDinLundbergProfile",
    "RollerBearingFlatProfile",
    "RollerBearingJohnsGoharProfile",
    "RollerBearingLundbergProfile",
    "RollerBearingProfile",
    "RollerBearingTangentialCrownedProfile",
    "RollerBearingUserSpecifiedProfile",
    "RollerRaceProfilePoint",
    "UserSpecifiedProfilePoint",
    "UserSpecifiedRollerRaceProfilePoint",
)
