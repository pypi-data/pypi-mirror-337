"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.gears._2712 import (
        ActiveCylindricalGearSetDesignSelection,
    )
    from mastapy._private.system_model.part_model.gears._2713 import (
        ActiveGearSetDesignSelection,
    )
    from mastapy._private.system_model.part_model.gears._2714 import (
        ActiveGearSetDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.gears._2715 import (
        AGMAGleasonConicalGear,
    )
    from mastapy._private.system_model.part_model.gears._2716 import (
        AGMAGleasonConicalGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2717 import (
        BevelDifferentialGear,
    )
    from mastapy._private.system_model.part_model.gears._2718 import (
        BevelDifferentialGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2719 import (
        BevelDifferentialPlanetGear,
    )
    from mastapy._private.system_model.part_model.gears._2720 import (
        BevelDifferentialSunGear,
    )
    from mastapy._private.system_model.part_model.gears._2721 import BevelGear
    from mastapy._private.system_model.part_model.gears._2722 import BevelGearSet
    from mastapy._private.system_model.part_model.gears._2723 import ConceptGear
    from mastapy._private.system_model.part_model.gears._2724 import ConceptGearSet
    from mastapy._private.system_model.part_model.gears._2725 import ConicalGear
    from mastapy._private.system_model.part_model.gears._2726 import ConicalGearSet
    from mastapy._private.system_model.part_model.gears._2727 import CylindricalGear
    from mastapy._private.system_model.part_model.gears._2728 import CylindricalGearSet
    from mastapy._private.system_model.part_model.gears._2729 import (
        CylindricalPlanetGear,
    )
    from mastapy._private.system_model.part_model.gears._2730 import FaceGear
    from mastapy._private.system_model.part_model.gears._2731 import FaceGearSet
    from mastapy._private.system_model.part_model.gears._2732 import Gear
    from mastapy._private.system_model.part_model.gears._2733 import GearOrientations
    from mastapy._private.system_model.part_model.gears._2734 import GearSet
    from mastapy._private.system_model.part_model.gears._2735 import (
        GearSetConfiguration,
    )
    from mastapy._private.system_model.part_model.gears._2736 import HypoidGear
    from mastapy._private.system_model.part_model.gears._2737 import HypoidGearSet
    from mastapy._private.system_model.part_model.gears._2738 import (
        KlingelnbergCycloPalloidConicalGear,
    )
    from mastapy._private.system_model.part_model.gears._2739 import (
        KlingelnbergCycloPalloidConicalGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2740 import (
        KlingelnbergCycloPalloidHypoidGear,
    )
    from mastapy._private.system_model.part_model.gears._2741 import (
        KlingelnbergCycloPalloidHypoidGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2742 import (
        KlingelnbergCycloPalloidSpiralBevelGear,
    )
    from mastapy._private.system_model.part_model.gears._2743 import (
        KlingelnbergCycloPalloidSpiralBevelGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2744 import PlanetaryGearSet
    from mastapy._private.system_model.part_model.gears._2745 import (
        ProfileToothDrawingMethod,
    )
    from mastapy._private.system_model.part_model.gears._2746 import SpiralBevelGear
    from mastapy._private.system_model.part_model.gears._2747 import SpiralBevelGearSet
    from mastapy._private.system_model.part_model.gears._2748 import (
        StraightBevelDiffGear,
    )
    from mastapy._private.system_model.part_model.gears._2749 import (
        StraightBevelDiffGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2750 import StraightBevelGear
    from mastapy._private.system_model.part_model.gears._2751 import (
        StraightBevelGearSet,
    )
    from mastapy._private.system_model.part_model.gears._2752 import (
        StraightBevelPlanetGear,
    )
    from mastapy._private.system_model.part_model.gears._2753 import (
        StraightBevelSunGear,
    )
    from mastapy._private.system_model.part_model.gears._2754 import WormGear
    from mastapy._private.system_model.part_model.gears._2755 import WormGearSet
    from mastapy._private.system_model.part_model.gears._2756 import ZerolBevelGear
    from mastapy._private.system_model.part_model.gears._2757 import ZerolBevelGearSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.gears._2712": [
            "ActiveCylindricalGearSetDesignSelection"
        ],
        "_private.system_model.part_model.gears._2713": [
            "ActiveGearSetDesignSelection"
        ],
        "_private.system_model.part_model.gears._2714": [
            "ActiveGearSetDesignSelectionGroup"
        ],
        "_private.system_model.part_model.gears._2715": ["AGMAGleasonConicalGear"],
        "_private.system_model.part_model.gears._2716": ["AGMAGleasonConicalGearSet"],
        "_private.system_model.part_model.gears._2717": ["BevelDifferentialGear"],
        "_private.system_model.part_model.gears._2718": ["BevelDifferentialGearSet"],
        "_private.system_model.part_model.gears._2719": ["BevelDifferentialPlanetGear"],
        "_private.system_model.part_model.gears._2720": ["BevelDifferentialSunGear"],
        "_private.system_model.part_model.gears._2721": ["BevelGear"],
        "_private.system_model.part_model.gears._2722": ["BevelGearSet"],
        "_private.system_model.part_model.gears._2723": ["ConceptGear"],
        "_private.system_model.part_model.gears._2724": ["ConceptGearSet"],
        "_private.system_model.part_model.gears._2725": ["ConicalGear"],
        "_private.system_model.part_model.gears._2726": ["ConicalGearSet"],
        "_private.system_model.part_model.gears._2727": ["CylindricalGear"],
        "_private.system_model.part_model.gears._2728": ["CylindricalGearSet"],
        "_private.system_model.part_model.gears._2729": ["CylindricalPlanetGear"],
        "_private.system_model.part_model.gears._2730": ["FaceGear"],
        "_private.system_model.part_model.gears._2731": ["FaceGearSet"],
        "_private.system_model.part_model.gears._2732": ["Gear"],
        "_private.system_model.part_model.gears._2733": ["GearOrientations"],
        "_private.system_model.part_model.gears._2734": ["GearSet"],
        "_private.system_model.part_model.gears._2735": ["GearSetConfiguration"],
        "_private.system_model.part_model.gears._2736": ["HypoidGear"],
        "_private.system_model.part_model.gears._2737": ["HypoidGearSet"],
        "_private.system_model.part_model.gears._2738": [
            "KlingelnbergCycloPalloidConicalGear"
        ],
        "_private.system_model.part_model.gears._2739": [
            "KlingelnbergCycloPalloidConicalGearSet"
        ],
        "_private.system_model.part_model.gears._2740": [
            "KlingelnbergCycloPalloidHypoidGear"
        ],
        "_private.system_model.part_model.gears._2741": [
            "KlingelnbergCycloPalloidHypoidGearSet"
        ],
        "_private.system_model.part_model.gears._2742": [
            "KlingelnbergCycloPalloidSpiralBevelGear"
        ],
        "_private.system_model.part_model.gears._2743": [
            "KlingelnbergCycloPalloidSpiralBevelGearSet"
        ],
        "_private.system_model.part_model.gears._2744": ["PlanetaryGearSet"],
        "_private.system_model.part_model.gears._2745": ["ProfileToothDrawingMethod"],
        "_private.system_model.part_model.gears._2746": ["SpiralBevelGear"],
        "_private.system_model.part_model.gears._2747": ["SpiralBevelGearSet"],
        "_private.system_model.part_model.gears._2748": ["StraightBevelDiffGear"],
        "_private.system_model.part_model.gears._2749": ["StraightBevelDiffGearSet"],
        "_private.system_model.part_model.gears._2750": ["StraightBevelGear"],
        "_private.system_model.part_model.gears._2751": ["StraightBevelGearSet"],
        "_private.system_model.part_model.gears._2752": ["StraightBevelPlanetGear"],
        "_private.system_model.part_model.gears._2753": ["StraightBevelSunGear"],
        "_private.system_model.part_model.gears._2754": ["WormGear"],
        "_private.system_model.part_model.gears._2755": ["WormGearSet"],
        "_private.system_model.part_model.gears._2756": ["ZerolBevelGear"],
        "_private.system_model.part_model.gears._2757": ["ZerolBevelGearSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveCylindricalGearSetDesignSelection",
    "ActiveGearSetDesignSelection",
    "ActiveGearSetDesignSelectionGroup",
    "AGMAGleasonConicalGear",
    "AGMAGleasonConicalGearSet",
    "BevelDifferentialGear",
    "BevelDifferentialGearSet",
    "BevelDifferentialPlanetGear",
    "BevelDifferentialSunGear",
    "BevelGear",
    "BevelGearSet",
    "ConceptGear",
    "ConceptGearSet",
    "ConicalGear",
    "ConicalGearSet",
    "CylindricalGear",
    "CylindricalGearSet",
    "CylindricalPlanetGear",
    "FaceGear",
    "FaceGearSet",
    "Gear",
    "GearOrientations",
    "GearSet",
    "GearSetConfiguration",
    "HypoidGear",
    "HypoidGearSet",
    "KlingelnbergCycloPalloidConicalGear",
    "KlingelnbergCycloPalloidConicalGearSet",
    "KlingelnbergCycloPalloidHypoidGear",
    "KlingelnbergCycloPalloidHypoidGearSet",
    "KlingelnbergCycloPalloidSpiralBevelGear",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
    "PlanetaryGearSet",
    "ProfileToothDrawingMethod",
    "SpiralBevelGear",
    "SpiralBevelGearSet",
    "StraightBevelDiffGear",
    "StraightBevelDiffGearSet",
    "StraightBevelGear",
    "StraightBevelGearSet",
    "StraightBevelPlanetGear",
    "StraightBevelSunGear",
    "WormGear",
    "WormGearSet",
    "ZerolBevelGear",
    "ZerolBevelGearSet",
)
