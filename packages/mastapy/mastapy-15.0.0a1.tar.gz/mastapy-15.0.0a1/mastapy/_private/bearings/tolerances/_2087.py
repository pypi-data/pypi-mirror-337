"""BearingConnectionComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_BEARING_CONNECTION_COMPONENT = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "BearingConnectionComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import (
        _2092,
        _2093,
        _2094,
        _2095,
        _2097,
        _2098,
        _2099,
        _2102,
        _2103,
        _2106,
        _2108,
    )

    Self = TypeVar("Self", bound="BearingConnectionComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingConnectionComponent._Cast_BearingConnectionComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingConnectionComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingConnectionComponent:
    """Special nested class for casting BearingConnectionComponent to subclasses."""

    __parent__: "BearingConnectionComponent"

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_2092.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _2092

        return self.__parent__._cast(_2092.InnerRingTolerance)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_2093.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _2093

        return self.__parent__._cast(_2093.InnerSupportTolerance)

    @property
    def interference_detail(self: "CastSelf") -> "_2094.InterferenceDetail":
        from mastapy._private.bearings.tolerances import _2094

        return self.__parent__._cast(_2094.InterferenceDetail)

    @property
    def interference_tolerance(self: "CastSelf") -> "_2095.InterferenceTolerance":
        from mastapy._private.bearings.tolerances import _2095

        return self.__parent__._cast(_2095.InterferenceTolerance)

    @property
    def mounting_sleeve_diameter_detail(
        self: "CastSelf",
    ) -> "_2097.MountingSleeveDiameterDetail":
        from mastapy._private.bearings.tolerances import _2097

        return self.__parent__._cast(_2097.MountingSleeveDiameterDetail)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_2098.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _2098

        return self.__parent__._cast(_2098.OuterRingTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_2099.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _2099

        return self.__parent__._cast(_2099.OuterSupportTolerance)

    @property
    def ring_detail(self: "CastSelf") -> "_2102.RingDetail":
        from mastapy._private.bearings.tolerances import _2102

        return self.__parent__._cast(_2102.RingDetail)

    @property
    def ring_tolerance(self: "CastSelf") -> "_2103.RingTolerance":
        from mastapy._private.bearings.tolerances import _2103

        return self.__parent__._cast(_2103.RingTolerance)

    @property
    def support_detail(self: "CastSelf") -> "_2106.SupportDetail":
        from mastapy._private.bearings.tolerances import _2106

        return self.__parent__._cast(_2106.SupportDetail)

    @property
    def support_tolerance(self: "CastSelf") -> "_2108.SupportTolerance":
        from mastapy._private.bearings.tolerances import _2108

        return self.__parent__._cast(_2108.SupportTolerance)

    @property
    def bearing_connection_component(self: "CastSelf") -> "BearingConnectionComponent":
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
class BearingConnectionComponent(_0.APIBase):
    """BearingConnectionComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_CONNECTION_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingConnectionComponent":
        """Cast to another type.

        Returns:
            _Cast_BearingConnectionComponent
        """
        return _Cast_BearingConnectionComponent(self)
