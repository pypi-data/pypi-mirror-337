"""DIN3990GearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.iso6336 import _595

_DIN3990_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.DIN3990", "DIN3990GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _448
    from mastapy._private.gears.rating.cylindrical import _549
    from mastapy._private.gears.rating.cylindrical.iso6336 import _601, _603

    Self = TypeVar("Self", bound="DIN3990GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DIN3990GearSingleFlankRating._Cast_DIN3990GearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN3990GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN3990GearSingleFlankRating:
    """Special nested class for casting DIN3990GearSingleFlankRating to subclasses."""

    __parent__: "DIN3990GearSingleFlankRating"

    @property
    def iso63361996_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_595.ISO63361996GearSingleFlankRating":
        return self.__parent__._cast(_595.ISO63361996GearSingleFlankRating)

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_603.ISO6336AbstractMetalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _603

        return self.__parent__._cast(_603.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_601.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _601

        return self.__parent__._cast(_601.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_549.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _549

        return self.__parent__._cast(_549.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_448.GearSingleFlankRating":
        from mastapy._private.gears.rating import _448

        return self.__parent__._cast(_448.GearSingleFlankRating)

    @property
    def din3990_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "DIN3990GearSingleFlankRating":
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
class DIN3990GearSingleFlankRating(_595.ISO63361996GearSingleFlankRating):
    """DIN3990GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN3990_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def relative_notch_sensitivity_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeNotchSensitivityFactorForStaticStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DIN3990GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_DIN3990GearSingleFlankRating
        """
        return _Cast_DIN3990GearSingleFlankRating(self)
