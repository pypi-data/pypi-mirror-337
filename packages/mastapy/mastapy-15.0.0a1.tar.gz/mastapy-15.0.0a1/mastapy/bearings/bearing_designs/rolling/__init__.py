"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2325 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2326 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2327 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2328 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2329 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2330 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2331 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2332 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2333 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2334 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2335 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2336 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2337 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2338 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2339 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2340 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2341 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2342 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2343 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2344 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2345 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2346 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2347 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2348 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2349 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2350 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2351 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2352 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2353 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2354 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2355 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2356 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2357 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2358 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2359 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2360 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2361 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2362 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2363 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2364 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2365 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2366 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2325": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2326": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2327": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2328": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2329": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2330": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2331": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2332": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2333": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2334": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2335": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2336": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2337": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2338": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2339": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2340": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2341": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2342": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2343": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2344": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2345": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2346": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2347": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2348": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2349": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2350": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2351": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2352": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2353": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2354": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2355": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2356": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2357": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2358": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2359": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2360": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2361": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2362": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2363": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2364": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2365": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2366": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
