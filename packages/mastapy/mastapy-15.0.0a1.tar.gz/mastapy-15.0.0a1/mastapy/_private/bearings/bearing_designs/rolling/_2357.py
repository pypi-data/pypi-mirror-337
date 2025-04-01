"""SelfAligningBallBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2330

_SELF_ALIGNING_BALL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SelfAligningBallBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2320, _2321, _2324
    from mastapy._private.bearings.bearing_designs.rolling import _2355

    Self = TypeVar("Self", bound="SelfAligningBallBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="SelfAligningBallBearing._Cast_SelfAligningBallBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SelfAligningBallBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SelfAligningBallBearing:
    """Special nested class for casting SelfAligningBallBearing to subclasses."""

    __parent__: "SelfAligningBallBearing"

    @property
    def ball_bearing(self: "CastSelf") -> "_2330.BallBearing":
        return self.__parent__._cast(_2330.BallBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2355.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2355

        return self.__parent__._cast(_2355.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2321.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2321

        return self.__parent__._cast(_2321.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2324.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2324

        return self.__parent__._cast(_2324.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2320.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2320

        return self.__parent__._cast(_2320.BearingDesign)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "SelfAligningBallBearing":
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
class SelfAligningBallBearing(_2330.BallBearing):
    """SelfAligningBallBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SELF_ALIGNING_BALL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def inner_ring_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_shoulder_diameter.setter
    @enforce_parameter_types
    def inner_ring_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingShoulderDiameter", value)

    @property
    def inner_ring_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_shoulder_height.setter
    @enforce_parameter_types
    def inner_ring_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SelfAligningBallBearing":
        """Cast to another type.

        Returns:
            _Cast_SelfAligningBallBearing
        """
        return _Cast_SelfAligningBallBearing(self)
