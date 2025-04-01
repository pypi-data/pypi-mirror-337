"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1375

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_CutoutShape")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_CutoutShape",)


class Overridable_CutoutShape(mixins.OverridableMixin, Enum):
    """Overridable_CutoutShape

    A specific implementation of 'Overridable' for 'CutoutShape' types.
    """

    __qualname__ = "CutoutShape"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_CutoutShape]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls: "Type[Overridable_CutoutShape]") -> "_1375.CutoutShape":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1375.CutoutShape
        """
        return _1375.CutoutShape

    @classmethod
    def implicit_type(cls: "Type[Overridable_CutoutShape]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1375.CutoutShape.type_()

    @property
    def value(self: "Self") -> "_1375.CutoutShape":
        """mastapy.electric_machines.CutoutShape

        Note:
            This property is readonly.
        """
        return None

    @property
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    def override_value(self: "Self") -> "_1375.CutoutShape":
        """mastapy.electric_machines.CutoutShape

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_1375.CutoutShape":
        """mastapy.electric_machines.CutoutShape

        Note:
            This property is readonly.
        """
        return None
