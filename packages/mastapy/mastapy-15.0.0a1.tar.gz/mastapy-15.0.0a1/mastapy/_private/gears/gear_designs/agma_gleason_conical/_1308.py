"""AGMAGleasonConicalGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.bevel import _1292
from mastapy._private.gears.gear_designs.conical import _1269

_AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical",
    "AGMAGleasonConicalGearSetDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _428, _431
    from mastapy._private.gears.gear_designs import _1045, _1047
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1307
    from mastapy._private.gears.gear_designs.bevel import _1295
    from mastapy._private.gears.gear_designs.conical import _1278
    from mastapy._private.gears.gear_designs.hypoid import _1084
    from mastapy._private.gears.gear_designs.spiral_bevel import _1068
    from mastapy._private.gears.gear_designs.straight_bevel import _1060
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1064
    from mastapy._private.gears.gear_designs.zerol_bevel import _1051
    from mastapy._private.gleason_smt_link import _388

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetDesign._Cast_AGMAGleasonConicalGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetDesign:
    """Special nested class for casting AGMAGleasonConicalGearSetDesign to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetDesign"

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1269.ConicalGearSetDesign":
        return self.__parent__._cast(_1269.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1047.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1047

        return self.__parent__._cast(_1047.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1045.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1045

        return self.__parent__._cast(_1045.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1051.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1051

        return self.__parent__._cast(_1051.ZerolBevelGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1060.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1060

        return self.__parent__._cast(_1060.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_1064.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1064

        return self.__parent__._cast(_1064.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1068.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1068

        return self.__parent__._cast(_1068.SpiralBevelGearSetDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1084.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1084

        return self.__parent__._cast(_1084.HypoidGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1295.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1295

        return self.__parent__._cast(_1295.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetDesign":
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
class AGMAGleasonConicalGearSetDesign(_1269.ConicalGearSetDesign):
    """AGMAGleasonConicalGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def crown_gear_to_cutter_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrownGearToCutterCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def design_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods]"""
        temp = pythonnet_property_get(self.wrapped, "DesignMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @design_method.setter
    @enforce_parameter_types
    def design_method(
        self: "Self", value: "_1292.AGMAGleasonConicalGearGeometryMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DesignMethod", value)

    @property
    def epicycloid_base_circle_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EpicycloidBaseCircleRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def gleason_minimum_factor_of_safety_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "GleasonMinimumFactorOfSafetyBending"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gleason_minimum_factor_of_safety_bending.setter
    @enforce_parameter_types
    def gleason_minimum_factor_of_safety_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "GleasonMinimumFactorOfSafetyBending", value
        )

    @property
    def gleason_minimum_factor_of_safety_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "GleasonMinimumFactorOfSafetyContact"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gleason_minimum_factor_of_safety_contact.setter
    @enforce_parameter_types
    def gleason_minimum_factor_of_safety_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "GleasonMinimumFactorOfSafetyContact", value
        )

    @property
    def input_module(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InputModule")

        if temp is None:
            return False

        return temp

    @input_module.setter
    @enforce_parameter_types
    def input_module(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "InputModule", bool(value) if value is not None else False
        )

    @property
    def manufacturing_method(self: "Self") -> "_388.CutterMethod":
        """mastapy.gleason_smt_link.CutterMethod"""
        temp = pythonnet_property_get(self.wrapped, "ManufacturingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.GleasonSMTLink.CutterMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gleason_smt_link._388", "CutterMethod"
        )(value)

    @manufacturing_method.setter
    @enforce_parameter_types
    def manufacturing_method(self: "Self", value: "_388.CutterMethod") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.GleasonSMTLink.CutterMethod"
        )
        pythonnet_property_set(self.wrapped, "ManufacturingMethod", value)

    @property
    def mean_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanNormalModule")

        if temp is None:
            return 0.0

        return temp

    @mean_normal_module.setter
    @enforce_parameter_types
    def mean_normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanNormalModule", float(value) if value is not None else 0.0
        )

    @property
    def number_of_blade_groups(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfBladeGroups")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_crown_gear_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCrownGearTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_offset_angle_in_root_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionOffsetAngleInRootPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    def pitch_limit_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchLimitPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def reliability_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @reliability_factor_bending.setter
    @enforce_parameter_types
    def reliability_factor_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ReliabilityFactorBending", value)

    @property
    def reliability_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @reliability_factor_contact.setter
    @enforce_parameter_types
    def reliability_factor_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ReliabilityFactorContact", value)

    @property
    def reliability_requirement_agma(self: "Self") -> "_428.SafetyRequirementsAGMA":
        """mastapy.gears.SafetyRequirementsAGMA"""
        temp = pythonnet_property_get(self.wrapped, "ReliabilityRequirementAGMA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.SafetyRequirementsAGMA"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._428", "SafetyRequirementsAGMA"
        )(value)

    @reliability_requirement_agma.setter
    @enforce_parameter_types
    def reliability_requirement_agma(
        self: "Self", value: "_428.SafetyRequirementsAGMA"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.SafetyRequirementsAGMA"
        )
        pythonnet_property_set(self.wrapped, "ReliabilityRequirementAGMA", value)

    @property
    def reliability_requirement_gleason(
        self: "Self",
    ) -> "_1278.GleasonSafetyRequirements":
        """mastapy.gears.gear_designs.conical.GleasonSafetyRequirements"""
        temp = pythonnet_property_get(self.wrapped, "ReliabilityRequirementGleason")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.GleasonSafetyRequirements"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1278",
            "GleasonSafetyRequirements",
        )(value)

    @reliability_requirement_gleason.setter
    @enforce_parameter_types
    def reliability_requirement_gleason(
        self: "Self", value: "_1278.GleasonSafetyRequirements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.GleasonSafetyRequirements"
        )
        pythonnet_property_set(self.wrapped, "ReliabilityRequirementGleason", value)

    @property
    def required_minimum_topland_to_module_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredMinimumToplandToModuleFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @required_minimum_topland_to_module_factor.setter
    @enforce_parameter_types
    def required_minimum_topland_to_module_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredMinimumToplandToModuleFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def tooth_taper(self: "Self") -> "_431.SpiralBevelToothTaper":
        """mastapy.gears.SpiralBevelToothTaper"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaper")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.SpiralBevelToothTaper"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._431", "SpiralBevelToothTaper"
        )(value)

    @tooth_taper.setter
    @enforce_parameter_types
    def tooth_taper(self: "Self", value: "_431.SpiralBevelToothTaper") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.SpiralBevelToothTaper"
        )
        pythonnet_property_set(self.wrapped, "ToothTaper", value)

    @property
    def wheel_involute_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInvoluteConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_involute_to_mean_cone_distance_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelInvoluteToMeanConeDistanceRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_involute_to_outer_cone_distance_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelInvoluteToOuterConeDistanceRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def conical_meshes(self: "Self") -> "List[_1307.AGMAGleasonConicalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.agma_gleason_conical.AGMAGleasonConicalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes(self: "Self") -> "List[_1307.AGMAGleasonConicalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.agma_gleason_conical.AGMAGleasonConicalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Meshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def export_ki_mo_skip_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportKIMoSKIPFile")

    def gleason_gemsxml_data(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GleasonGEMSXMLData")

    def ki_mo_sxml_data(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "KIMoSXMLData")

    def store_ki_mo_skip_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "StoreKIMoSKIPFile")

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetDesign
        """
        return _Cast_AGMAGleasonConicalGearSetDesign(self)
