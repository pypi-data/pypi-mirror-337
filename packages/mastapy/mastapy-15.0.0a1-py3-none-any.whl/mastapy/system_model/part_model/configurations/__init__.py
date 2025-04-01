"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2822 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2823 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2824 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2825 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2826 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2827 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2828 import (
        DesignConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2829 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2830 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2822": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2823": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2824": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2825": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2826": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2827": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2828": [
            "DesignConfiguration"
        ],
        "_private.system_model.part_model.configurations._2829": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2830": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "DesignConfiguration",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
