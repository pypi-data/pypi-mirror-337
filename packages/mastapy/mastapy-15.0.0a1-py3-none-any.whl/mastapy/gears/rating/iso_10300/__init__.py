"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.iso_10300._504 import (
        GeneralLoadFactorCalculationMethod,
    )
    from mastapy._private.gears.rating.iso_10300._505 import Iso10300FinishingMethods
    from mastapy._private.gears.rating.iso_10300._506 import (
        ISO10300MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.iso_10300._507 import (
        ISO10300MeshSingleFlankRatingBevelMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._508 import (
        ISO10300MeshSingleFlankRatingHypoidMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._509 import (
        ISO10300MeshSingleFlankRatingMethodB1,
    )
    from mastapy._private.gears.rating.iso_10300._510 import (
        ISO10300MeshSingleFlankRatingMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._511 import ISO10300RateableMesh
    from mastapy._private.gears.rating.iso_10300._512 import ISO10300RatingMethod
    from mastapy._private.gears.rating.iso_10300._513 import ISO10300SingleFlankRating
    from mastapy._private.gears.rating.iso_10300._514 import (
        ISO10300SingleFlankRatingBevelMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._515 import (
        ISO10300SingleFlankRatingHypoidMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._516 import (
        ISO10300SingleFlankRatingMethodB1,
    )
    from mastapy._private.gears.rating.iso_10300._517 import (
        ISO10300SingleFlankRatingMethodB2,
    )
    from mastapy._private.gears.rating.iso_10300._518 import (
        MountingConditionsOfPinionAndWheel,
    )
    from mastapy._private.gears.rating.iso_10300._519 import (
        PittingFactorCalculationMethod,
    )
    from mastapy._private.gears.rating.iso_10300._520 import ProfileCrowningSetting
    from mastapy._private.gears.rating.iso_10300._521 import (
        VerificationOfContactPattern,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.iso_10300._504": ["GeneralLoadFactorCalculationMethod"],
        "_private.gears.rating.iso_10300._505": ["Iso10300FinishingMethods"],
        "_private.gears.rating.iso_10300._506": ["ISO10300MeshSingleFlankRating"],
        "_private.gears.rating.iso_10300._507": [
            "ISO10300MeshSingleFlankRatingBevelMethodB2"
        ],
        "_private.gears.rating.iso_10300._508": [
            "ISO10300MeshSingleFlankRatingHypoidMethodB2"
        ],
        "_private.gears.rating.iso_10300._509": [
            "ISO10300MeshSingleFlankRatingMethodB1"
        ],
        "_private.gears.rating.iso_10300._510": [
            "ISO10300MeshSingleFlankRatingMethodB2"
        ],
        "_private.gears.rating.iso_10300._511": ["ISO10300RateableMesh"],
        "_private.gears.rating.iso_10300._512": ["ISO10300RatingMethod"],
        "_private.gears.rating.iso_10300._513": ["ISO10300SingleFlankRating"],
        "_private.gears.rating.iso_10300._514": [
            "ISO10300SingleFlankRatingBevelMethodB2"
        ],
        "_private.gears.rating.iso_10300._515": [
            "ISO10300SingleFlankRatingHypoidMethodB2"
        ],
        "_private.gears.rating.iso_10300._516": ["ISO10300SingleFlankRatingMethodB1"],
        "_private.gears.rating.iso_10300._517": ["ISO10300SingleFlankRatingMethodB2"],
        "_private.gears.rating.iso_10300._518": ["MountingConditionsOfPinionAndWheel"],
        "_private.gears.rating.iso_10300._519": ["PittingFactorCalculationMethod"],
        "_private.gears.rating.iso_10300._520": ["ProfileCrowningSetting"],
        "_private.gears.rating.iso_10300._521": ["VerificationOfContactPattern"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GeneralLoadFactorCalculationMethod",
    "Iso10300FinishingMethods",
    "ISO10300MeshSingleFlankRating",
    "ISO10300MeshSingleFlankRatingBevelMethodB2",
    "ISO10300MeshSingleFlankRatingHypoidMethodB2",
    "ISO10300MeshSingleFlankRatingMethodB1",
    "ISO10300MeshSingleFlankRatingMethodB2",
    "ISO10300RateableMesh",
    "ISO10300RatingMethod",
    "ISO10300SingleFlankRating",
    "ISO10300SingleFlankRatingBevelMethodB2",
    "ISO10300SingleFlankRatingHypoidMethodB2",
    "ISO10300SingleFlankRatingMethodB1",
    "ISO10300SingleFlankRatingMethodB2",
    "MountingConditionsOfPinionAndWheel",
    "PittingFactorCalculationMethod",
    "ProfileCrowningSetting",
    "VerificationOfContactPattern",
)
