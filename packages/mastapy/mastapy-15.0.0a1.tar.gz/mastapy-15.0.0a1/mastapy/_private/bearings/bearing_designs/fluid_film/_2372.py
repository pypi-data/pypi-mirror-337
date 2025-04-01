"""AxialFeedJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_AXIAL_FEED_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "AxialFeedJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs.fluid_film import _2373, _2374

    Self = TypeVar("Self", bound="AxialFeedJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="AxialFeedJournalBearing._Cast_AxialFeedJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AxialFeedJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AxialFeedJournalBearing:
    """Special nested class for casting AxialFeedJournalBearing to subclasses."""

    __parent__: "AxialFeedJournalBearing"

    @property
    def axial_groove_journal_bearing(
        self: "CastSelf",
    ) -> "_2373.AxialGrooveJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2373

        return self.__parent__._cast(_2373.AxialGrooveJournalBearing)

    @property
    def axial_hole_journal_bearing(self: "CastSelf") -> "_2374.AxialHoleJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2374

        return self.__parent__._cast(_2374.AxialHoleJournalBearing)

    @property
    def axial_feed_journal_bearing(self: "CastSelf") -> "AxialFeedJournalBearing":
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
class AxialFeedJournalBearing(_0.APIBase):
    """AxialFeedJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AXIAL_FEED_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def groove_angular_location(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GrooveAngularLocation")

        if temp is None:
            return 0.0

        return temp

    @groove_angular_location.setter
    @enforce_parameter_types
    def groove_angular_location(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GrooveAngularLocation",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AxialFeedJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_AxialFeedJournalBearing
        """
        return _Cast_AxialFeedJournalBearing(self)
