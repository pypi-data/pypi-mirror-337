"""ThreeDViewContourOptionSecondSelection"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_THREE_D_VIEW_CONTOUR_OPTION_SECOND_SELECTION = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "ThreeDViewContourOptionSecondSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThreeDViewContourOptionSecondSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThreeDViewContourOptionSecondSelection._Cast_ThreeDViewContourOptionSecondSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDViewContourOptionSecondSelection",)


class ThreeDViewContourOptionSecondSelection(Enum):
    """ThreeDViewContourOptionSecondSelection

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _THREE_D_VIEW_CONTOUR_OPTION_SECOND_SELECTION

    PER_COMPONENT = 0
    PER_ELEMENT = 1
    PER_FE_SECTION = 2
    ANGULAR_MAGNITUDE = 3
    RADIAL_TILT_MAGNITUDE = 4
    TWIST = 5
    LINEAR_MAGNITUDE = 6
    RADIAL_MAGNITUDE = 7
    AXIAL = 8
    LOCAL_X = 9
    LOCAL_Y = 10
    LOCAL_Z = 11
    TORQUE = 12
    NOMINAL_AXIAL = 13
    NOMINAL_BENDING = 14
    NOMINAL_TORSIONAL = 15
    NOMINAL_VON_MISES_ALTERNATING = 16
    NOMINAL_VON_MISES_MAX = 17
    NOMINAL_VON_MISES_MEAN = 18
    NOMINAL_MAXIMUM_PRINCIPAL = 19
    NOMINAL_MINIMUM_PRINCIPAL = 20
    NORMAL_DISPLACEMENT = 21
    NORMAL_VELOCITY = 22
    NORMAL_ACCELERATION = 23


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ThreeDViewContourOptionSecondSelection.__setattr__ = __enum_setattr
ThreeDViewContourOptionSecondSelection.__delattr__ = __enum_delattr
