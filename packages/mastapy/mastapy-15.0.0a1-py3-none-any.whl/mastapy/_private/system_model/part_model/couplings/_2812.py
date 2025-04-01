"""SpringDamperHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.couplings import _2789

_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2662, _2666

    Self = TypeVar("Self", bound="SpringDamperHalf")
    CastSelf = TypeVar("CastSelf", bound="SpringDamperHalf._Cast_SpringDamperHalf")


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperHalf:
    """Special nested class for casting SpringDamperHalf to subclasses."""

    __parent__: "SpringDamperHalf"

    @property
    def coupling_half(self: "CastSelf") -> "_2789.CouplingHalf":
        return self.__parent__._cast(_2789.CouplingHalf)

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
        from mastapy._private.system_model.part_model import _2662

        return self.__parent__._cast(_2662.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        from mastapy._private.system_model.part_model import _2639

        return self.__parent__._cast(_2639.Component)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def spring_damper_half(self: "CastSelf") -> "SpringDamperHalf":
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
class SpringDamperHalf(_2789.CouplingHalf):
    """SpringDamperHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamperHalf":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperHalf
        """
        return _Cast_SpringDamperHalf(self)
