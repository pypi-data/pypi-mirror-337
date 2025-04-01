"""ReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "ReliefWithDeviation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1220,
        _1222,
        _1223,
        _1224,
        _1234,
        _1236,
        _1237,
        _1238,
        _1241,
        _1242,
    )

    Self = TypeVar("Self", bound="ReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf", bound="ReliefWithDeviation._Cast_ReliefWithDeviation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReliefWithDeviation:
    """Special nested class for casting ReliefWithDeviation to subclasses."""

    __parent__: "ReliefWithDeviation"

    @property
    def lead_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1220.LeadFormReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1220

        return self.__parent__._cast(_1220.LeadFormReliefWithDeviation)

    @property
    def lead_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "_1222.LeadReliefSpecificationForCustomer102":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1222

        return self.__parent__._cast(_1222.LeadReliefSpecificationForCustomer102)

    @property
    def lead_relief_with_deviation(self: "CastSelf") -> "_1223.LeadReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1223

        return self.__parent__._cast(_1223.LeadReliefWithDeviation)

    @property
    def lead_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1224.LeadSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1224

        return self.__parent__._cast(_1224.LeadSlopeReliefWithDeviation)

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
    def profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1237.ProfileReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1237

        return self.__parent__._cast(_1237.ProfileReliefWithDeviation)

    @property
    def profile_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1238.ProfileSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1238

        return self.__parent__._cast(_1238.ProfileSlopeReliefWithDeviation)

    @property
    def total_lead_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1241.TotalLeadReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1241

        return self.__parent__._cast(_1241.TotalLeadReliefWithDeviation)

    @property
    def total_profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1242.TotalProfileReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1242

        return self.__parent__._cast(_1242.TotalProfileReliefWithDeviation)

    @property
    def relief_with_deviation(self: "CastSelf") -> "ReliefWithDeviation":
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
class ReliefWithDeviation(_0.APIBase):
    """ReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def lower_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowerLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Relief")

        if temp is None:
            return 0.0

        return temp

    @property
    def section(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Section")

        if temp is None:
            return ""

        return temp

    @property
    def upper_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpperLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_ReliefWithDeviation
        """
        return _Cast_ReliefWithDeviation(self)
