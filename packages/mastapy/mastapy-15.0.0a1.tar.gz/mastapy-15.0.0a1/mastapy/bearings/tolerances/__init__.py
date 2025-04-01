"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._2087 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._2088 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._2089 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._2090 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._2091 import FitType
    from mastapy._private.bearings.tolerances._2092 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._2093 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._2094 import InterferenceDetail
    from mastapy._private.bearings.tolerances._2095 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._2096 import ITDesignation
    from mastapy._private.bearings.tolerances._2097 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._2098 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._2099 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._2100 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._2101 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._2102 import RingDetail
    from mastapy._private.bearings.tolerances._2103 import RingTolerance
    from mastapy._private.bearings.tolerances._2104 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._2105 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._2106 import SupportDetail
    from mastapy._private.bearings.tolerances._2107 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._2108 import SupportTolerance
    from mastapy._private.bearings.tolerances._2109 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._2110 import ToleranceCombination
    from mastapy._private.bearings.tolerances._2111 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._2087": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._2088": ["InternalClearanceClass"],
        "_private.bearings.tolerances._2089": ["BearingToleranceClass"],
        "_private.bearings.tolerances._2090": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._2091": ["FitType"],
        "_private.bearings.tolerances._2092": ["InnerRingTolerance"],
        "_private.bearings.tolerances._2093": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._2094": ["InterferenceDetail"],
        "_private.bearings.tolerances._2095": ["InterferenceTolerance"],
        "_private.bearings.tolerances._2096": ["ITDesignation"],
        "_private.bearings.tolerances._2097": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._2098": ["OuterRingTolerance"],
        "_private.bearings.tolerances._2099": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._2100": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._2101": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._2102": ["RingDetail"],
        "_private.bearings.tolerances._2103": ["RingTolerance"],
        "_private.bearings.tolerances._2104": ["RoundnessSpecification"],
        "_private.bearings.tolerances._2105": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._2106": ["SupportDetail"],
        "_private.bearings.tolerances._2107": ["SupportMaterialSource"],
        "_private.bearings.tolerances._2108": ["SupportTolerance"],
        "_private.bearings.tolerances._2109": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._2110": ["ToleranceCombination"],
        "_private.bearings.tolerances._2111": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
