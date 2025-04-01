"""ProfileReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1239

_PROFILE_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "ProfileReliefWithDeviation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1128
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1234,
        _1236,
        _1238,
        _1242,
    )

    Self = TypeVar("Self", bound="ProfileReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf", bound="ProfileReliefWithDeviation._Cast_ProfileReliefWithDeviation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileReliefWithDeviation:
    """Special nested class for casting ProfileReliefWithDeviation to subclasses."""

    __parent__: "ProfileReliefWithDeviation"

    @property
    def relief_with_deviation(self: "CastSelf") -> "_1239.ReliefWithDeviation":
        return self.__parent__._cast(_1239.ReliefWithDeviation)

    @property
    def profile_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1234.ProfileFormReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1234

        return self.__parent__._cast(_1234.ProfileFormReliefWithDeviation)

    @property
    def profile_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "_1236.ProfileReliefSpecificationForCustomer102":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1236

        return self.__parent__._cast(_1236.ProfileReliefSpecificationForCustomer102)

    @property
    def profile_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1238.ProfileSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1238

        return self.__parent__._cast(_1238.ProfileSlopeReliefWithDeviation)

    @property
    def total_profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1242.TotalProfileReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1242

        return self.__parent__._cast(_1242.TotalProfileReliefWithDeviation)

    @property
    def profile_relief_with_deviation(self: "CastSelf") -> "ProfileReliefWithDeviation":
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
class ProfileReliefWithDeviation(_1239.ReliefWithDeviation):
    """ProfileReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def profile_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    def roll_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def position_on_profile(self: "Self") -> "_1128.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionOnProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_ProfileReliefWithDeviation
        """
        return _Cast_ProfileReliefWithDeviation(self)
