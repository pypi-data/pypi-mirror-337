"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.property._2022 import DeletableCollectionMember
    from mastapy._private.utility.property._2023 import DutyCyclePropertySummary
    from mastapy._private.utility.property._2024 import DutyCyclePropertySummaryForce
    from mastapy._private.utility.property._2025 import (
        DutyCyclePropertySummaryPercentage,
    )
    from mastapy._private.utility.property._2026 import (
        DutyCyclePropertySummarySmallAngle,
    )
    from mastapy._private.utility.property._2027 import DutyCyclePropertySummaryStress
    from mastapy._private.utility.property._2028 import (
        DutyCyclePropertySummaryVeryShortLength,
    )
    from mastapy._private.utility.property._2029 import EnumWithBoolean
    from mastapy._private.utility.property._2030 import (
        NamedRangeWithOverridableMinAndMax,
    )
    from mastapy._private.utility.property._2031 import TypedObjectsWithOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.property._2022": ["DeletableCollectionMember"],
        "_private.utility.property._2023": ["DutyCyclePropertySummary"],
        "_private.utility.property._2024": ["DutyCyclePropertySummaryForce"],
        "_private.utility.property._2025": ["DutyCyclePropertySummaryPercentage"],
        "_private.utility.property._2026": ["DutyCyclePropertySummarySmallAngle"],
        "_private.utility.property._2027": ["DutyCyclePropertySummaryStress"],
        "_private.utility.property._2028": ["DutyCyclePropertySummaryVeryShortLength"],
        "_private.utility.property._2029": ["EnumWithBoolean"],
        "_private.utility.property._2030": ["NamedRangeWithOverridableMinAndMax"],
        "_private.utility.property._2031": ["TypedObjectsWithOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DeletableCollectionMember",
    "DutyCyclePropertySummary",
    "DutyCyclePropertySummaryForce",
    "DutyCyclePropertySummaryPercentage",
    "DutyCyclePropertySummarySmallAngle",
    "DutyCyclePropertySummaryStress",
    "DutyCyclePropertySummaryVeryShortLength",
    "EnumWithBoolean",
    "NamedRangeWithOverridableMinAndMax",
    "TypedObjectsWithOption",
)
