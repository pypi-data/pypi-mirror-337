"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.generics._1990 import NamedTuple1
    from mastapy._private.utility.generics._1991 import NamedTuple2
    from mastapy._private.utility.generics._1992 import NamedTuple3
    from mastapy._private.utility.generics._1993 import NamedTuple4
    from mastapy._private.utility.generics._1994 import NamedTuple5
    from mastapy._private.utility.generics._1995 import NamedTuple6
    from mastapy._private.utility.generics._1996 import NamedTuple7
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.generics._1990": ["NamedTuple1"],
        "_private.utility.generics._1991": ["NamedTuple2"],
        "_private.utility.generics._1992": ["NamedTuple3"],
        "_private.utility.generics._1993": ["NamedTuple4"],
        "_private.utility.generics._1994": ["NamedTuple5"],
        "_private.utility.generics._1995": ["NamedTuple6"],
        "_private.utility.generics._1996": ["NamedTuple7"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "NamedTuple1",
    "NamedTuple2",
    "NamedTuple3",
    "NamedTuple4",
    "NamedTuple5",
    "NamedTuple6",
    "NamedTuple7",
)
