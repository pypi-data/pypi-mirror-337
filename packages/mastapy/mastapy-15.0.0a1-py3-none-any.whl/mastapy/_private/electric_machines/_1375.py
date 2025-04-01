"""CutoutShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CUTOUT_SHAPE = python_net_import("SMT.MastaAPI.ElectricMachines", "CutoutShape")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CutoutShape")
    CastSelf = TypeVar("CastSelf", bound="CutoutShape._Cast_CutoutShape")


__docformat__ = "restructuredtext en"
__all__ = ("CutoutShape",)


class CutoutShape(Enum):
    """CutoutShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CUTOUT_SHAPE

    RECTANGLE = 0
    CIRCLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CutoutShape.__setattr__ = __enum_setattr
CutoutShape.__delattr__ = __enum_delattr
