"""CylindricalGearFlankMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.micro_geometry import _654

_CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearFlankMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1115, _1128
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1199,
        _1202,
        _1209,
        _1211,
        _1216,
        _1220,
        _1224,
        _1234,
        _1238,
        _1241,
        _1242,
    )
    from mastapy._private.math_utility.measured_data import _1739

    Self = TypeVar("Self", bound="CylindricalGearFlankMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFlankMicroGeometry._Cast_CylindricalGearFlankMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankMicroGeometry:
    """Special nested class for casting CylindricalGearFlankMicroGeometry to subclasses."""

    __parent__: "CylindricalGearFlankMicroGeometry"

    @property
    def flank_micro_geometry(self: "CastSelf") -> "_654.FlankMicroGeometry":
        return self.__parent__._cast(_654.FlankMicroGeometry)

    @property
    def cylindrical_gear_flank_micro_geometry(
        self: "CastSelf",
    ) -> "CylindricalGearFlankMicroGeometry":
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
class CylindricalGearFlankMicroGeometry(_654.FlankMicroGeometry):
    """CylindricalGearFlankMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def micro_geometry_matrix(self: "Self") -> "_1739.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryMatrix")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @micro_geometry_matrix.setter
    @enforce_parameter_types
    def micro_geometry_matrix(
        self: "Self", value: "_1739.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "MicroGeometryMatrix", value.wrapped)

    @property
    def modified_normal_pressure_angle_due_to_helix_angle_modification_assuming_unmodified_normal_module_and_pressure_angle_modification(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModuleAndPressureAngleModification",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def use_measured_map_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredMapData")

        if temp is None:
            return False

        return temp

    @use_measured_map_data.setter
    @enforce_parameter_types
    def use_measured_map_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMeasuredMapData",
            bool(value) if value is not None else False,
        )

    @property
    def bias(self: "Self") -> "_1199.CylindricalGearBiasModification":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearBiasModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bias")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def lead_relief(self: "Self") -> "_1202.CylindricalGearLeadModification":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearLeadModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def micro_geometry_map(self: "Self") -> "_1209.CylindricalGearMicroGeometryMap":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMicroGeometryMap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryMap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def profile_control_point(
        self: "Self",
    ) -> "_1128.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileControlPoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def profile_relief(self: "Self") -> "_1211.CylindricalGearProfileModification":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearProfileModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def triangular_end_relief(
        self: "Self",
    ) -> "_1216.CylindricalGearTriangularEndModification":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearTriangularEndModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TriangularEndRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def lead_form_deviation_points(
        self: "Self",
    ) -> "List[_1220.LeadFormReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.LeadFormReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadFormDeviationPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def lead_slope_deviation_points(
        self: "Self",
    ) -> "List[_1224.LeadSlopeReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.LeadSlopeReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadSlopeDeviationPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def profile_form_deviation_points(
        self: "Self",
    ) -> "List[_1234.ProfileFormReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileFormReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileFormDeviationPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def profile_slope_deviation_at_10_percent_face_width(
        self: "Self",
    ) -> "List[_1238.ProfileSlopeReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileSlopeReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileSlopeDeviationAt10PercentFaceWidth"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def profile_slope_deviation_at_50_percent_face_width(
        self: "Self",
    ) -> "List[_1238.ProfileSlopeReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileSlopeReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileSlopeDeviationAt50PercentFaceWidth"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def profile_slope_deviation_at_90_percent_face_width(
        self: "Self",
    ) -> "List[_1238.ProfileSlopeReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileSlopeReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileSlopeDeviationAt90PercentFaceWidth"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def total_lead_relief_points(
        self: "Self",
    ) -> "List[_1241.TotalLeadReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.TotalLeadReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLeadReliefPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def total_profile_relief_points(
        self: "Self",
    ) -> "List[_1242.TotalProfileReliefWithDeviation]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.TotalProfileReliefWithDeviation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalProfileReliefPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gear_design(self: "Self") -> "_1115.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def total_relief(
        self: "Self", face_width: "float", roll_distance: "float"
    ) -> "float":
        """float

        Args:
            face_width (float)
            roll_distance (float)
        """
        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TotalRelief",
            face_width if face_width else 0.0,
            roll_distance if roll_distance else 0.0,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankMicroGeometry
        """
        return _Cast_CylindricalGearFlankMicroGeometry(self)
