"""RollingBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2056, _2057, _2078, _2081
from mastapy._private.bearings.bearing_designs import _2321
from mastapy._private.bearings.bearing_designs.rolling import _2341, _2342, _2348, _2366

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ROLLING_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollingBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2055, _2058, _2063
    from mastapy._private.bearings.bearing_designs import _2320, _2324
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2325,
        _2326,
        _2327,
        _2328,
        _2329,
        _2330,
        _2332,
        _2333,
        _2336,
        _2337,
        _2338,
        _2339,
        _2340,
        _2344,
        _2345,
        _2349,
        _2350,
        _2351,
        _2352,
        _2356,
        _2357,
        _2358,
        _2359,
        _2360,
        _2361,
        _2362,
        _2363,
        _2364,
        _2365,
    )
    from mastapy._private.bearings.bearing_results.rolling import _2165
    from mastapy._private.materials import _326
    from mastapy._private.utility import _1757

    Self = TypeVar("Self", bound="RollingBearing")
    CastSelf = TypeVar("CastSelf", bound="RollingBearing._Cast_RollingBearing")


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearing:
    """Special nested class for casting RollingBearing to subclasses."""

    __parent__: "RollingBearing"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2321.DetailedBearing":
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
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2325.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2325

        return self.__parent__._cast(_2325.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2326.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2326

        return self.__parent__._cast(_2326.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2327.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2327

        return self.__parent__._cast(_2327.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2328.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2328

        return self.__parent__._cast(_2328.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2329.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2329

        return self.__parent__._cast(_2329.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2330.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2330

        return self.__parent__._cast(_2330.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2332.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2332

        return self.__parent__._cast(_2332.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2338.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2338

        return self.__parent__._cast(_2338.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2339.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2339

        return self.__parent__._cast(_2339.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2340.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2340

        return self.__parent__._cast(_2340.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2344.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2344

        return self.__parent__._cast(_2344.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2349.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2349

        return self.__parent__._cast(_2349.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2350.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2350

        return self.__parent__._cast(_2350.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2351.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2351

        return self.__parent__._cast(_2351.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2352.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2352

        return self.__parent__._cast(_2352.RollerBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2357.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2357

        return self.__parent__._cast(_2357.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2360.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2360

        return self.__parent__._cast(_2360.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2361.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2361

        return self.__parent__._cast(_2361.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2362.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2362

        return self.__parent__._cast(_2362.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2363.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2363

        return self.__parent__._cast(_2363.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2364.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2364

        return self.__parent__._cast(_2364.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2365.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2365

        return self.__parent__._cast(_2365.ToroidalRollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "RollingBearing":
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
class RollingBearing(_2321.DetailedBearing):
    """RollingBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def are_the_inner_rings_a_single_piece_of_metal(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "AreTheInnerRingsASinglePieceOfMetal"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @are_the_inner_rings_a_single_piece_of_metal.setter
    @enforce_parameter_types
    def are_the_inner_rings_a_single_piece_of_metal(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AreTheInnerRingsASinglePieceOfMetal", value
        )

    @property
    def are_the_outer_rings_a_single_piece_of_metal(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "AreTheOuterRingsASinglePieceOfMetal"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @are_the_outer_rings_a_single_piece_of_metal.setter
    @enforce_parameter_types
    def are_the_outer_rings_a_single_piece_of_metal(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AreTheOuterRingsASinglePieceOfMetal", value
        )

    @property
    def arrangement(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingArrangement]"""
        temp = pythonnet_property_get(self.wrapped, "Arrangement")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @arrangement.setter
    @enforce_parameter_types
    def arrangement(self: "Self", value: "_2078.RollingBearingArrangement") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Arrangement", value)

    @property
    def basic_dynamic_load_rating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRating")

        if temp is None:
            return 0.0

        return temp

    @basic_dynamic_load_rating.setter
    @enforce_parameter_types
    def basic_dynamic_load_rating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BasicDynamicLoadRating",
            float(value) if value is not None else 0.0,
        )

    @property
    def basic_dynamic_load_rating_calculation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod":
        """EnumWithSelectedValue[mastapy.bearings.BasicDynamicLoadRatingCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRatingCalculation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @basic_dynamic_load_rating_calculation.setter
    @enforce_parameter_types
    def basic_dynamic_load_rating_calculation(
        self: "Self", value: "_2056.BasicDynamicLoadRatingCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BasicDynamicLoadRatingCalculation", value)

    @property
    def basic_dynamic_load_rating_divided_by_correction_factors(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingDividedByCorrectionFactors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_dynamic_load_rating_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRatingSource")

        if temp is None:
            return ""

        return temp

    @property
    def basic_static_load_rating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRating")

        if temp is None:
            return 0.0

        return temp

    @basic_static_load_rating.setter
    @enforce_parameter_types
    def basic_static_load_rating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BasicStaticLoadRating",
            float(value) if value is not None else 0.0,
        )

    @property
    def basic_static_load_rating_calculation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod":
        """EnumWithSelectedValue[mastapy.bearings.BasicStaticLoadRatingCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingCalculation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @basic_static_load_rating_calculation.setter
    @enforce_parameter_types
    def basic_static_load_rating_calculation(
        self: "Self", value: "_2057.BasicStaticLoadRatingCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BasicStaticLoadRatingCalculation", value)

    @property
    def basic_static_load_rating_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_static_load_rating_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingSource")

        if temp is None:
            return ""

        return temp

    @property
    def cage_bridge_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_angle.setter
    @enforce_parameter_types
    def cage_bridge_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeAngle", value)

    @property
    def cage_bridge_axial_surface_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeAxialSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_axial_surface_radius.setter
    @enforce_parameter_types
    def cage_bridge_axial_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeAxialSurfaceRadius", value)

    @property
    def cage_bridge_radial_surface_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeRadialSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_radial_surface_radius.setter
    @enforce_parameter_types
    def cage_bridge_radial_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeRadialSurfaceRadius", value)

    @property
    def cage_bridge_shape(self: "Self") -> "_2337.CageBridgeShape":
        """mastapy.bearings.bearing_designs.rolling.CageBridgeShape"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.CageBridgeShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2337", "CageBridgeShape"
        )(value)

    @cage_bridge_shape.setter
    @enforce_parameter_types
    def cage_bridge_shape(self: "Self", value: "_2337.CageBridgeShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.CageBridgeShape"
        )
        pythonnet_property_set(self.wrapped, "CageBridgeShape", value)

    @property
    def cage_bridge_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageBridgeWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cage_guiding_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageGuidingRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_guiding_ring_width.setter
    @enforce_parameter_types
    def cage_guiding_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageGuidingRingWidth", value)

    @property
    def cage_mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageMass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_mass.setter
    @enforce_parameter_types
    def cage_mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageMass", value)

    @property
    def cage_material(self: "Self") -> "_2058.BearingCageMaterial":
        """mastapy.bearings.BearingCageMaterial"""
        temp = pythonnet_property_get(self.wrapped, "CageMaterial")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingCageMaterial"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2058", "BearingCageMaterial"
        )(value)

    @cage_material.setter
    @enforce_parameter_types
    def cage_material(self: "Self", value: "_2058.BearingCageMaterial") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingCageMaterial"
        )
        pythonnet_property_set(self.wrapped, "CageMaterial", value)

    @property
    def cage_pitch_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CagePitchRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_pitch_radius.setter
    @enforce_parameter_types
    def cage_pitch_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CagePitchRadius", value)

    @property
    def cage_pocket_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CagePocketClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_pocket_clearance.setter
    @enforce_parameter_types
    def cage_pocket_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CagePocketClearance", value)

    @property
    def cage_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_thickness.setter
    @enforce_parameter_types
    def cage_thickness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageThickness", value)

    @property
    def cage_to_inner_ring_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageToInnerRingClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_to_inner_ring_clearance.setter
    @enforce_parameter_types
    def cage_to_inner_ring_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageToInnerRingClearance", value)

    @property
    def cage_to_outer_ring_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageToOuterRingClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_to_outer_ring_clearance.setter
    @enforce_parameter_types
    def cage_to_outer_ring_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageToOuterRingClearance", value)

    @property
    def cage_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_width.setter
    @enforce_parameter_types
    def cage_width(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageWidth", value)

    @property
    def catalogue(self: "Self") -> "_2055.BearingCatalog":
        """mastapy.bearings.BearingCatalog

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Catalogue")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingCatalog")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2055", "BearingCatalog"
        )(value)

    @property
    def combined_surface_roughness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedSurfaceRoughnessInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def combined_surface_roughness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedSurfaceRoughnessOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContactAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contact_angle.setter
    @enforce_parameter_types
    def contact_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactAngle", value)

    @property
    def contact_radius_in_rolling_direction_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusInRollingDirectionInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_radius_in_rolling_direction_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusInRollingDirectionOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def designation(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Designation")

        if temp is None:
            return ""

        return temp

    @designation.setter
    @enforce_parameter_types
    def designation(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Designation", str(value) if value is not None else ""
        )

    @property
    def diameter_series(self: "Self") -> "overridable.Overridable_DiameterSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.DiameterSeries]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterSeries")

        if temp is None:
            return None

        value = overridable.Overridable_DiameterSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @diameter_series.setter
    @enforce_parameter_types
    def diameter_series(
        self: "Self",
        value: "Union[_2341.DiameterSeries, Tuple[_2341.DiameterSeries, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_DiameterSeries.wrapper_type()
        enclosed_type = overridable.Overridable_DiameterSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterSeries", value)

    @property
    def distance_between_element_centres(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenElementCentres")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_element_centres.setter
    @enforce_parameter_types
    def distance_between_element_centres(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DistanceBetweenElementCentres", value)

    @property
    def dynamic_axial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicAxialLoadFactorForHighAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_axial_load_factor_for_high_axial_radial_load_ratios.setter
    @enforce_parameter_types
    def dynamic_axial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicAxialLoadFactorForHighAxialRadialLoadRatios", value
        )

    @property
    def dynamic_axial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicAxialLoadFactorForLowAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_axial_load_factor_for_low_axial_radial_load_ratios.setter
    @enforce_parameter_types
    def dynamic_axial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicAxialLoadFactorForLowAxialRadialLoadRatios", value
        )

    @property
    def dynamic_equivalent_load_factors_can_be_specified(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicEquivalentLoadFactorsCanBeSpecified"
        )

        if temp is None:
            return False

        return temp

    @property
    def dynamic_radial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicRadialLoadFactorForHighAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_radial_load_factor_for_high_axial_radial_load_ratios.setter
    @enforce_parameter_types
    def dynamic_radial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicRadialLoadFactorForHighAxialRadialLoadRatios", value
        )

    @property
    def dynamic_radial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicRadialLoadFactorForLowAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_radial_load_factor_for_low_axial_radial_load_ratios.setter
    @enforce_parameter_types
    def dynamic_radial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicRadialLoadFactorForLowAxialRadialLoadRatios", value
        )

    @property
    def element_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_diameter.setter
    @enforce_parameter_types
    def element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementDiameter", value)

    @property
    def element_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ElementMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @element_material_reportable.setter
    @enforce_parameter_types
    def element_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ElementMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def element_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_offset.setter
    @enforce_parameter_types
    def element_offset(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementOffset", value)

    @property
    def element_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_surface_roughness_rms(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSurfaceRoughnessRMS")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_surface_roughness_rms.setter
    @enforce_parameter_types
    def element_surface_roughness_rms(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSurfaceRoughnessRMS", value)

    @property
    def element_surface_roughness_ra(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSurfaceRoughnessRa")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_surface_roughness_ra.setter
    @enforce_parameter_types
    def element_surface_roughness_ra(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSurfaceRoughnessRa", value)

    @property
    def extra_information(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtraInformation")

        if temp is None:
            return ""

        return temp

    @property
    def factor_for_basic_dynamic_load_rating_in_ansiabma(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FactorForBasicDynamicLoadRatingInANSIABMA"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def fatigue_load_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FatigueLoadLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_load_limit.setter
    @enforce_parameter_types
    def fatigue_load_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FatigueLoadLimit", value)

    @property
    def fatigue_load_limit_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum":
        """EnumWithSelectedValue[mastapy.bearings.bearing_designs.rolling.FatigueLoadLimitCalculationMethodEnum]"""
        temp = pythonnet_property_get(self.wrapped, "FatigueLoadLimitCalculationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @fatigue_load_limit_calculation_method.setter
    @enforce_parameter_types
    def fatigue_load_limit_calculation_method(
        self: "Self", value: "_2342.FatigueLoadLimitCalculationMethodEnum"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FatigueLoadLimitCalculationMethod", value)

    @property
    def free_space_between_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FreeSpaceBetweenElements")

        if temp is None:
            return 0.0

        return temp

    @property
    def height_series(self: "Self") -> "overridable.Overridable_HeightSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.HeightSeries]"""
        temp = pythonnet_property_get(self.wrapped, "HeightSeries")

        if temp is None:
            return None

        value = overridable.Overridable_HeightSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @height_series.setter
    @enforce_parameter_types
    def height_series(
        self: "Self",
        value: "Union[_2348.HeightSeries, Tuple[_2348.HeightSeries, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_HeightSeries.wrapper_type()
        enclosed_type = overridable.Overridable_HeightSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HeightSeries", value)

    @property
    def iso_material_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ISOMaterialFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @iso_material_factor.setter
    @enforce_parameter_types
    def iso_material_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ISOMaterialFactor", value)

    @property
    def inner_race_hardness_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRaceHardnessDepth")

        if temp is None:
            return 0.0

        return temp

    @inner_race_hardness_depth.setter
    @enforce_parameter_types
    def inner_race_hardness_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRaceHardnessDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_race_outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceOuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def inner_ring_left_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingLeftCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_left_corner_radius.setter
    @enforce_parameter_types
    def inner_ring_left_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingLeftCornerRadius", value)

    @property
    def inner_ring_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InnerRingMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @inner_ring_material_reportable.setter
    @enforce_parameter_types
    def inner_ring_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InnerRingMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def inner_ring_right_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingRightCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_right_corner_radius.setter
    @enforce_parameter_types
    def inner_ring_right_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingRightCornerRadius", value)

    @property
    def inner_ring_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingRaceType]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @inner_ring_type.setter
    @enforce_parameter_types
    def inner_ring_type(self: "Self", value: "_2081.RollingBearingRaceType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "InnerRingType", value)

    @property
    def inner_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_width.setter
    @enforce_parameter_types
    def inner_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingWidth", value)

    @property
    def is_full_complement(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IsFullComplement")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @is_full_complement.setter
    @enforce_parameter_types
    def is_full_complement(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IsFullComplement", value)

    @property
    def is_network_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsNetworkItem")

        if temp is None:
            return False

        return temp

    @is_network_item.setter
    @enforce_parameter_types
    def is_network_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsNetworkItem", bool(value) if value is not None else False
        )

    @property
    def kz(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KZ")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @kz.setter
    @enforce_parameter_types
    def kz(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KZ", value)

    @property
    def limiting_value_for_axial_load_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LimitingValueForAxialLoadRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @limiting_value_for_axial_load_ratio.setter
    @enforce_parameter_types
    def limiting_value_for_axial_load_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LimitingValueForAxialLoadRatio", value)

    @property
    def manufacturer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Manufacturer")

        if temp is None:
            return ""

        return temp

    @manufacturer.setter
    @enforce_parameter_types
    def manufacturer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Manufacturer", str(value) if value is not None else ""
        )

    @property
    def maximum_grease_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumGreaseSpeed")

        if temp is None:
            return 0.0

        return temp

    @maximum_grease_speed.setter
    @enforce_parameter_types
    def maximum_grease_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumGreaseSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_oil_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumOilSpeed")

        if temp is None:
            return 0.0

        return temp

    @maximum_oil_speed.setter
    @enforce_parameter_types
    def maximum_oil_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumOilSpeed", float(value) if value is not None else 0.0
        )

    @property
    def maximum_permissible_contact_stress_for_static_failure_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureInner"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_permissible_contact_stress_for_static_failure_inner.setter
    @enforce_parameter_types
    def maximum_permissible_contact_stress_for_static_failure_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureInner", value
        )

    @property
    def maximum_permissible_contact_stress_for_static_failure_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureOuter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_permissible_contact_stress_for_static_failure_outer.setter
    @enforce_parameter_types
    def maximum_permissible_contact_stress_for_static_failure_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureOuter", value
        )

    @property
    def minimum_surface_roughness_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSurfaceRoughnessRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_surface_roughness_ra(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSurfaceRoughnessRa")

        if temp is None:
            return 0.0

        return temp

    @property
    def model(self: "Self") -> "_2063.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2063", "BearingModel"
        )(value)

    @property
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    def number_of_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_elements.setter
    @enforce_parameter_types
    def number_of_elements(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfElements", value)

    @property
    def number_of_rows(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRows")

        if temp is None:
            return 0

        return temp

    @number_of_rows.setter
    @enforce_parameter_types
    def number_of_rows(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfRows", int(value) if value is not None else 0
        )

    @property
    def outer_race_hardness_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRaceHardnessDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_race_hardness_depth.setter
    @enforce_parameter_types
    def outer_race_hardness_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRaceHardnessDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_race_inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceInnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def outer_ring_left_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingLeftCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_left_corner_radius.setter
    @enforce_parameter_types
    def outer_ring_left_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingLeftCornerRadius", value)

    @property
    def outer_ring_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "OuterRingMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @outer_ring_material_reportable.setter
    @enforce_parameter_types
    def outer_ring_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "OuterRingMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    def outer_ring_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_offset.setter
    @enforce_parameter_types
    def outer_ring_offset(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingOffset", value)

    @property
    def outer_ring_right_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingRightCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_right_corner_radius.setter
    @enforce_parameter_types
    def outer_ring_right_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingRightCornerRadius", value)

    @property
    def outer_ring_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingRaceType]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @outer_ring_type.setter
    @enforce_parameter_types
    def outer_ring_type(self: "Self", value: "_2081.RollingBearingRaceType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "OuterRingType", value)

    @property
    def outer_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_width.setter
    @enforce_parameter_types
    def outer_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingWidth", value)

    @property
    def pitch_circle_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PitchCircleDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pitch_circle_diameter.setter
    @enforce_parameter_types
    def pitch_circle_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PitchCircleDiameter", value)

    @property
    def power_for_maximum_contact_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerForMaximumContactStressSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def raceway_surface_roughness_rms_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRMSInner")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_rms_inner.setter
    @enforce_parameter_types
    def raceway_surface_roughness_rms_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRMSInner", value)

    @property
    def raceway_surface_roughness_rms_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRMSOuter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_rms_outer.setter
    @enforce_parameter_types
    def raceway_surface_roughness_rms_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRMSOuter", value)

    @property
    def raceway_surface_roughness_ra_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRaInner")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_ra_inner.setter
    @enforce_parameter_types
    def raceway_surface_roughness_ra_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRaInner", value)

    @property
    def raceway_surface_roughness_ra_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRaOuter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_ra_outer.setter
    @enforce_parameter_types
    def raceway_surface_roughness_ra_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRaOuter", value)

    @property
    def sleeve_type(self: "Self") -> "_2359.SleeveType":
        """mastapy.bearings.bearing_designs.rolling.SleeveType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SleeveType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.SleeveType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2359", "SleeveType"
        )(value)

    @property
    def theoretical_maximum_number_of_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TheoreticalMaximumNumberOfElements"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_free_space_between_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalFreeSpaceBetweenElements")

        if temp is None:
            return 0.0

        return temp

    @property
    def type_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return ""

        return temp

    @property
    def type_information(self: "Self") -> "_2336.BearingTypeExtraInformation":
        """mastapy.bearings.bearing_designs.rolling.BearingTypeExtraInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TypeInformation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.BearingTypeExtraInformation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2336",
            "BearingTypeExtraInformation",
        )(value)

    @property
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def width_series(self: "Self") -> "overridable.Overridable_WidthSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.WidthSeries]"""
        temp = pythonnet_property_get(self.wrapped, "WidthSeries")

        if temp is None:
            return None

        value = overridable.Overridable_WidthSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @width_series.setter
    @enforce_parameter_types
    def width_series(
        self: "Self", value: "Union[_2366.WidthSeries, Tuple[_2366.WidthSeries, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_WidthSeries.wrapper_type()
        enclosed_type = overridable.Overridable_WidthSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WidthSeries", value)

    @property
    def element_material(self: "Self") -> "_326.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def geometric_constants(self: "Self") -> "_2345.GeometricConstants":
        """mastapy.bearings.bearing_designs.rolling.GeometricConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometricConstants")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def history(self: "Self") -> "_1757.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso153122018(self: "Self") -> "_2165.ISO153122018Results":
        """mastapy.bearings.bearing_results.rolling.ISO153122018Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO153122018")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_ring_material(self: "Self") -> "_326.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRingMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_ring_material(self: "Self") -> "_326.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRingMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def protection(self: "Self") -> "_2333.BearingProtection":
        """mastapy.bearings.bearing_designs.rolling.BearingProtection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Protection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def skf_seal_frictional_moment_constants(
        self: "Self",
    ) -> "_2358.SKFSealFrictionalMomentConstants":
        """mastapy.bearings.bearing_designs.rolling.SKFSealFrictionalMomentConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFSealFrictionalMomentConstants")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def elements(self: "Self") -> "List[_2356.RollingBearingElement]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearingElement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Elements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def remove_inner_ring_while_keeping_other_geometry_constant(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "RemoveInnerRingWhileKeepingOtherGeometryConstant"
        )

    def remove_outer_ring_while_keeping_other_geometry_constant(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "RemoveOuterRingWhileKeepingOtherGeometryConstant"
        )

    def __copy__(self: "Self") -> "RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def __deepcopy__(self: "Self", memo) -> "RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def link_to_online_catalogue(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LinkToOnlineCatalogue")

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearing":
        """Cast to another type.

        Returns:
            _Cast_RollingBearing
        """
        return _Cast_RollingBearing(self)
