"""CylindricalGearDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _441

_CYLINDRICAL_GEAR_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1328
    from mastapy._private.gears.rating import _437, _442
    from mastapy._private.gears.rating.cylindrical import _544, _547, _559

    Self = TypeVar("Self", bound="CylindricalGearDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDutyCycleRating._Cast_CylindricalGearDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDutyCycleRating:
    """Special nested class for casting CylindricalGearDutyCycleRating to subclasses."""

    __parent__: "CylindricalGearDutyCycleRating"

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_441.GearDutyCycleRating":
        return self.__parent__._cast(_441.GearDutyCycleRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_437.AbstractGearRating":
        from mastapy._private.gears.rating import _437

        return self.__parent__._cast(_437.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1328.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1328

        return self.__parent__._cast(_1328.AbstractGearAnalysis)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "CylindricalGearDutyCycleRating":
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
class CylindricalGearDutyCycleRating(_441.GearDutyCycleRating):
    """CylindricalGearDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def highest_maximum_material_exposure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestMaximumMaterialExposure")

        if temp is None:
            return 0.0

        return temp

    @property
    def safety_factor_against_permanent_deformation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorAgainstPermanentDeformation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def safety_factor_against_permanent_deformation_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_set_design_duty_cycle(
        self: "Self",
    ) -> "_547.CylindricalGearSetDutyCycleRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesignDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_set_design_duty_cycle(
        self: "Self",
    ) -> "_547.CylindricalGearSetDutyCycleRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSetDesignDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def left_flank_rating(self: "Self") -> "_442.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def right_flank_rating(self: "Self") -> "_442.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_mesh_ratings(
        self: "Self",
    ) -> "List[_559.MeshRatingForReports]":
        """List[mastapy.gears.rating.cylindrical.MeshRatingForReports]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gear_ratings(self: "Self") -> "List[_544.CylindricalGearRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gear_ratings(self: "Self") -> "List[_544.CylindricalGearRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDutyCycleRating
        """
        return _Cast_CylindricalGearDutyCycleRating(self)
