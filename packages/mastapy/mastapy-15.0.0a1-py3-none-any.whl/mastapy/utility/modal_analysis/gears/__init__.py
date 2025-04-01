"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.modal_analysis.gears._1977 import GearMeshForTE
    from mastapy._private.utility.modal_analysis.gears._1978 import GearOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1979 import GearPositions
    from mastapy._private.utility.modal_analysis.gears._1980 import HarmonicOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1981 import LabelOnlyOrder
    from mastapy._private.utility.modal_analysis.gears._1982 import OrderForTE
    from mastapy._private.utility.modal_analysis.gears._1983 import OrderSelector
    from mastapy._private.utility.modal_analysis.gears._1984 import OrderWithRadius
    from mastapy._private.utility.modal_analysis.gears._1985 import RollingBearingOrder
    from mastapy._private.utility.modal_analysis.gears._1986 import ShaftOrderForTE
    from mastapy._private.utility.modal_analysis.gears._1987 import (
        UserDefinedOrderForTE,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.modal_analysis.gears._1977": ["GearMeshForTE"],
        "_private.utility.modal_analysis.gears._1978": ["GearOrderForTE"],
        "_private.utility.modal_analysis.gears._1979": ["GearPositions"],
        "_private.utility.modal_analysis.gears._1980": ["HarmonicOrderForTE"],
        "_private.utility.modal_analysis.gears._1981": ["LabelOnlyOrder"],
        "_private.utility.modal_analysis.gears._1982": ["OrderForTE"],
        "_private.utility.modal_analysis.gears._1983": ["OrderSelector"],
        "_private.utility.modal_analysis.gears._1984": ["OrderWithRadius"],
        "_private.utility.modal_analysis.gears._1985": ["RollingBearingOrder"],
        "_private.utility.modal_analysis.gears._1986": ["ShaftOrderForTE"],
        "_private.utility.modal_analysis.gears._1987": ["UserDefinedOrderForTE"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
