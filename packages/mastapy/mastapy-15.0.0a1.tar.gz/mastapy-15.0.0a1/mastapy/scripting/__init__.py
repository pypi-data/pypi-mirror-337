"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7862 import ApiEnumForAttribute
    from mastapy._private.scripting._7863 import ApiVersion
    from mastapy._private.scripting._7864 import SMTBitmap
    from mastapy._private.scripting._7866 import MastaPropertyAttribute
    from mastapy._private.scripting._7867 import PythonCommand
    from mastapy._private.scripting._7868 import ScriptingCommand
    from mastapy._private.scripting._7869 import ScriptingExecutionCommand
    from mastapy._private.scripting._7870 import ScriptingObjectCommand
    from mastapy._private.scripting._7871 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7862": ["ApiEnumForAttribute"],
        "_private.scripting._7863": ["ApiVersion"],
        "_private.scripting._7864": ["SMTBitmap"],
        "_private.scripting._7866": ["MastaPropertyAttribute"],
        "_private.scripting._7867": ["PythonCommand"],
        "_private.scripting._7868": ["ScriptingCommand"],
        "_private.scripting._7869": ["ScriptingExecutionCommand"],
        "_private.scripting._7870": ["ScriptingObjectCommand"],
        "_private.scripting._7871": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
