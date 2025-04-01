"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.process_simulation._735 import (
        CutterProcessSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.process_simulation._736 import (
        FormWheelGrindingProcessSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.process_simulation._737 import (
        ShapingProcessSimulation,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.process_simulation._735": [
            "CutterProcessSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.process_simulation._736": [
            "FormWheelGrindingProcessSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.process_simulation._737": [
            "ShapingProcessSimulation"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterProcessSimulation",
    "FormWheelGrindingProcessSimulation",
    "ShapingProcessSimulation",
)
