"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _742

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_MicroGeometryDefinitionType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_MicroGeometryDefinitionType",)


class EnumWithSelectedValue_MicroGeometryDefinitionType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_MicroGeometryDefinitionType

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionType' types.
    """

    __qualname__ = "MicroGeometryDefinitionType"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionType]",
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
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionType]",
    ) -> "_742.MicroGeometryDefinitionType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _742.MicroGeometryDefinitionType
        """
        return _742.MicroGeometryDefinitionType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_MicroGeometryDefinitionType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _742.MicroGeometryDefinitionType.type_()

    @property
    def selected_value(self: "Self") -> "_742.MicroGeometryDefinitionType":
        """mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_742.MicroGeometryDefinitionType]":
        """List[mastapy.gears.manufacturing.cylindrical.plunge_shaving.MicroGeometryDefinitionType]

        Note:
            This property is readonly.
        """
        return None
