"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1594

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_SplineToleranceClassTypes")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_SplineToleranceClassTypes",)


class EnumWithSelectedValue_SplineToleranceClassTypes(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_SplineToleranceClassTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineToleranceClassTypes' types.
    """

    __qualname__ = "SplineToleranceClassTypes"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_SplineToleranceClassTypes]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_SplineToleranceClassTypes]",
    ) -> "_1594.SplineToleranceClassTypes":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1594.SplineToleranceClassTypes
        """
        return _1594.SplineToleranceClassTypes

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_SplineToleranceClassTypes]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1594.SplineToleranceClassTypes.type_()

    @property
    def selected_value(self: "Self") -> "_1594.SplineToleranceClassTypes":
        """mastapy.detailed_rigid_connectors.splines.SplineToleranceClassTypes

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1594.SplineToleranceClassTypes]":
        """List[mastapy.detailed_rigid_connectors.splines.SplineToleranceClassTypes]

        Note:
            This property is readonly.
        """
        return None
