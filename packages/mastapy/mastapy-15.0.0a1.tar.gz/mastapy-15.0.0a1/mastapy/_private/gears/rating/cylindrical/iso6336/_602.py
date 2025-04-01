"""ISO6336AbstractMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical import _551

_ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ISO6336AbstractMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _450
    from mastapy._private.gears.rating.cylindrical import _562
    from mastapy._private.gears.rating.cylindrical.din3990 import _617
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _596,
        _598,
        _600,
        _601,
        _604,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _574,
        _576,
        _578,
    )

    Self = TypeVar("Self", bound="ISO6336AbstractMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336AbstractMeshSingleFlankRating._Cast_ISO6336AbstractMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336AbstractMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336AbstractMeshSingleFlankRating:
    """Special nested class for casting ISO6336AbstractMeshSingleFlankRating to subclasses."""

    __parent__: "ISO6336AbstractMeshSingleFlankRating"

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_551.CylindricalMeshSingleFlankRating":
        return self.__parent__._cast(_551.CylindricalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_450.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _450

        return self.__parent__._cast(_450.MeshSingleFlankRating)

    @property
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_574.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _574

        return self.__parent__._cast(
            _574.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_576.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _576

        return self.__parent__._cast(
            _576.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_578.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _578

        return self.__parent__._cast(_578.PlasticPlasticVDI2736MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_596.ISO63361996MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _596

        return self.__parent__._cast(_596.ISO63361996MeshSingleFlankRating)

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_598.ISO63362006MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _598

        return self.__parent__._cast(_598.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_600.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _600

        return self.__parent__._cast(_600.ISO63362019MeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_604.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _604

        return self.__parent__._cast(_604.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_617.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _617

        return self.__parent__._cast(_617.DIN3990MeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO6336AbstractMeshSingleFlankRating":
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
class ISO6336AbstractMeshSingleFlankRating(_551.CylindricalMeshSingleFlankRating):
    """ISO6336AbstractMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_ABSTRACT_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def application_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_ratio_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_ratio_factor_for_nominal_root_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRatioFactorForNominalRootRootStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorSource")

        if temp is None:
            return ""

        return temp

    @property
    def elasticity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_contact_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContactSource")

        if temp is None:
            return ""

        return temp

    @property
    def helix_angle_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def helix_angle_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def misalignment_contact_pattern_enhancement(
        self: "Self",
    ) -> "_562.MisalignmentContactPatternEnhancements":
        """mastapy.gears.rating.cylindrical.MisalignmentContactPatternEnhancements

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentContactPatternEnhancement"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.MisalignmentContactPatternEnhancements",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical._562",
            "MisalignmentContactPatternEnhancements",
        )(value)

    @property
    def nominal_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_velocity_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingVelocityAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_velocity_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocityAtPitchPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_velocity_at_start_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingVelocityAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sum_of_tangential_velocities_at_end_of_active_profile(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtEndOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sum_of_tangential_velocities_at_pitch_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtPitchPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sum_of_tangential_velocities_at_start_of_active_profile(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfTangentialVelocitiesAtStartOfActiveProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def zone_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZoneFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_601.ISO6336AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def isodin_cylindrical_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_601.ISO6336AbstractGearSingleFlankRating]":
        """List[mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISODINCylindricalGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336AbstractMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO6336AbstractMeshSingleFlankRating
        """
        return _Cast_ISO6336AbstractMeshSingleFlankRating(self)
