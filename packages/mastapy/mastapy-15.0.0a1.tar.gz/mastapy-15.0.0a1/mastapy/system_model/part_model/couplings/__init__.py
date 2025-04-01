"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2780 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2781 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2782 import Clutch
    from mastapy._private.system_model.part_model.couplings._2783 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2784 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2785 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2786 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2787 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2788 import Coupling
    from mastapy._private.system_model.part_model.couplings._2789 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2790 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2791 import CVT
    from mastapy._private.system_model.part_model.couplings._2792 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2793 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2794 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2795 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2796 import Pulley
    from mastapy._private.system_model.part_model.couplings._2797 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2798 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2799 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2800 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2801 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2802 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2803 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2804 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2805 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2806 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2807 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2808 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2809 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2810 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2811 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2812 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2813 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2814 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2815 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2816 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2817 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2818 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2819 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2820 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2821 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2780": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2781": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2782": ["Clutch"],
        "_private.system_model.part_model.couplings._2783": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2784": ["ClutchType"],
        "_private.system_model.part_model.couplings._2785": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2786": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2787": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2788": ["Coupling"],
        "_private.system_model.part_model.couplings._2789": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2790": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2791": ["CVT"],
        "_private.system_model.part_model.couplings._2792": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2793": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2794": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2795": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2796": ["Pulley"],
        "_private.system_model.part_model.couplings._2797": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2798": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2799": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2800": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2801": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2802": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2803": ["RollingRing"],
        "_private.system_model.part_model.couplings._2804": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2805": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2806": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2807": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2808": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2809": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2810": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2811": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2812": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2813": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2814": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2815": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2816": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2817": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2818": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2819": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2820": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2821": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
