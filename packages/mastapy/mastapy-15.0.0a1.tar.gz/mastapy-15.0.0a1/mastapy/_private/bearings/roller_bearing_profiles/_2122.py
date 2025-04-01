"""RollerBearingProfile"""

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

_ROLLER_BEARING_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.roller_bearing_profiles import (
        _2116,
        _2117,
        _2118,
        _2119,
        _2120,
        _2121,
        _2123,
        _2124,
    )

    Self = TypeVar("Self", bound="RollerBearingProfile")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerBearingProfile._Cast_RollerBearingProfile"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingProfile:
    """Special nested class for casting RollerBearingProfile to subclasses."""

    __parent__: "RollerBearingProfile"

    @property
    def roller_bearing_conical_profile(
        self: "CastSelf",
    ) -> "_2116.RollerBearingConicalProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2116

        return self.__parent__._cast(_2116.RollerBearingConicalProfile)

    @property
    def roller_bearing_crowned_profile(
        self: "CastSelf",
    ) -> "_2117.RollerBearingCrownedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2117

        return self.__parent__._cast(_2117.RollerBearingCrownedProfile)

    @property
    def roller_bearing_din_lundberg_profile(
        self: "CastSelf",
    ) -> "_2118.RollerBearingDinLundbergProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2118

        return self.__parent__._cast(_2118.RollerBearingDinLundbergProfile)

    @property
    def roller_bearing_flat_profile(
        self: "CastSelf",
    ) -> "_2119.RollerBearingFlatProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2119

        return self.__parent__._cast(_2119.RollerBearingFlatProfile)

    @property
    def roller_bearing_johns_gohar_profile(
        self: "CastSelf",
    ) -> "_2120.RollerBearingJohnsGoharProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2120

        return self.__parent__._cast(_2120.RollerBearingJohnsGoharProfile)

    @property
    def roller_bearing_lundberg_profile(
        self: "CastSelf",
    ) -> "_2121.RollerBearingLundbergProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2121

        return self.__parent__._cast(_2121.RollerBearingLundbergProfile)

    @property
    def roller_bearing_tangential_crowned_profile(
        self: "CastSelf",
    ) -> "_2123.RollerBearingTangentialCrownedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2123

        return self.__parent__._cast(_2123.RollerBearingTangentialCrownedProfile)

    @property
    def roller_bearing_user_specified_profile(
        self: "CastSelf",
    ) -> "_2124.RollerBearingUserSpecifiedProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2124

        return self.__parent__._cast(_2124.RollerBearingUserSpecifiedProfile)

    @property
    def roller_bearing_profile(self: "CastSelf") -> "RollerBearingProfile":
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
class RollerBearingProfile(_0.APIBase):
    """RollerBearingProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def covers_two_rows_of_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CoversTwoRowsOfElements")

        if temp is None:
            return False

        return temp

    @covers_two_rows_of_elements.setter
    @enforce_parameter_types
    def covers_two_rows_of_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoversTwoRowsOfElements",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingProfile
        """
        return _Cast_RollerBearingProfile(self)
