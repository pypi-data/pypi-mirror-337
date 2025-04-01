"""ComplexMatrix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1689

_COMPLEX_MATRIX = python_net_import("SMT.MastaAPI.MathUtility", "ComplexMatrix")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1671, _1672, _1673

    Self = TypeVar("Self", bound="ComplexMatrix")
    CastSelf = TypeVar("CastSelf", bound="ComplexMatrix._Cast_ComplexMatrix")


__docformat__ = "restructuredtext en"
__all__ = ("ComplexMatrix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComplexMatrix:
    """Special nested class for casting ComplexMatrix to subclasses."""

    __parent__: "ComplexMatrix"

    @property
    def generic_matrix(self: "CastSelf") -> "_1689.GenericMatrix":
        pass

        return self.__parent__._cast(_1689.GenericMatrix)

    @property
    def complex_vector(self: "CastSelf") -> "_1671.ComplexVector":
        from mastapy._private.math_utility import _1671

        return self.__parent__._cast(_1671.ComplexVector)

    @property
    def complex_vector_3d(self: "CastSelf") -> "_1672.ComplexVector3D":
        from mastapy._private.math_utility import _1672

        return self.__parent__._cast(_1672.ComplexVector3D)

    @property
    def complex_vector_6d(self: "CastSelf") -> "_1673.ComplexVector6D":
        from mastapy._private.math_utility import _1673

        return self.__parent__._cast(_1673.ComplexVector6D)

    @property
    def complex_matrix(self: "CastSelf") -> "ComplexMatrix":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class ComplexMatrix(_1689.GenericMatrix[complex, "ComplexMatrix"]):
    """ComplexMatrix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPLEX_MATRIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ComplexMatrix":
        """Cast to another type.

        Returns:
            _Cast_ComplexMatrix
        """
        return _Cast_ComplexMatrix(self)
