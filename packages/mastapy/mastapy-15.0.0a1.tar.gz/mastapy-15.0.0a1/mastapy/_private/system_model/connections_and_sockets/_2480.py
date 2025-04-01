"""PlanetarySocketBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2467

_PLANETARY_SOCKET_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetarySocketBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _423
    from mastapy._private.system_model.connections_and_sockets import _2479, _2487
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2530

    Self = TypeVar("Self", bound="PlanetarySocketBase")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetarySocketBase._Cast_PlanetarySocketBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetarySocketBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetarySocketBase:
    """Special nested class for casting PlanetarySocketBase to subclasses."""

    __parent__: "PlanetarySocketBase"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2467.CylindricalSocket":
        return self.__parent__._cast(_2467.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2487.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2487

        return self.__parent__._cast(_2487.Socket)

    @property
    def planetary_socket(self: "CastSelf") -> "_2479.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2479

        return self.__parent__._cast(_2479.PlanetarySocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2530.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2530,
        )

        return self.__parent__._cast(_2530.CycloidalDiscPlanetaryBearingSocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "PlanetarySocketBase":
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
class PlanetarySocketBase(_2467.CylindricalSocket):
    """PlanetarySocketBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_SOCKET_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def draw_on_lower_half_of_2d(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawOnLowerHalfOf2D")

        if temp is None:
            return False

        return temp

    @draw_on_lower_half_of_2d.setter
    @enforce_parameter_types
    def draw_on_lower_half_of_2d(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawOnLowerHalfOf2D",
            bool(value) if value is not None else False,
        )

    @property
    def draw_on_upper_half_of_2d(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawOnUpperHalfOf2D")

        if temp is None:
            return False

        return temp

    @draw_on_upper_half_of_2d.setter
    @enforce_parameter_types
    def draw_on_upper_half_of_2d(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawOnUpperHalfOf2D",
            bool(value) if value is not None else False,
        )

    @property
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
        )

    @property
    def planetary_load_sharing_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PlanetaryLoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @planetary_load_sharing_factor.setter
    @enforce_parameter_types
    def planetary_load_sharing_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlanetaryLoadSharingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def planetary_details(self: "Self") -> "_423.PlanetaryDetail":
        """mastapy.gears.PlanetaryDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetarySocketBase":
        """Cast to another type.

        Returns:
            _Cast_PlanetarySocketBase
        """
        return _Cast_PlanetarySocketBase(self)
