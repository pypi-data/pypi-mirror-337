"""SphericalRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2332

_SPHERICAL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SphericalRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2320, _2321, _2324
    from mastapy._private.bearings.bearing_designs.rolling import _2352, _2355

    Self = TypeVar("Self", bound="SphericalRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="SphericalRollerBearing._Cast_SphericalRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SphericalRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SphericalRollerBearing:
    """Special nested class for casting SphericalRollerBearing to subclasses."""

    __parent__: "SphericalRollerBearing"

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2332.BarrelRollerBearing":
        return self.__parent__._cast(_2332.BarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2352.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2352

        return self.__parent__._cast(_2352.RollerBearing)

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
    def spherical_roller_bearing(self: "CastSelf") -> "SphericalRollerBearing":
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
class SphericalRollerBearing(_2332.BarrelRollerBearing):
    """SphericalRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPHERICAL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SphericalRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_SphericalRollerBearing
        """
        return _Cast_SphericalRollerBearing(self)
