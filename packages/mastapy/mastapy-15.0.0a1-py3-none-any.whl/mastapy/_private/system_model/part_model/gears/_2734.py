"""GearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1047
from mastapy._private.system_model.part_model import _2676

_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2629, _2666
    from mastapy._private.system_model.part_model.gears import (
        _2716,
        _2718,
        _2722,
        _2724,
        _2726,
        _2728,
        _2731,
        _2737,
        _2739,
        _2741,
        _2743,
        _2744,
        _2747,
        _2749,
        _2751,
        _2755,
        _2757,
    )

    Self = TypeVar("Self", bound="GearSet")
    CastSelf = TypeVar("CastSelf", bound="GearSet._Cast_GearSet")


__docformat__ = "restructuredtext en"
__all__ = ("GearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSet:
    """Special nested class for casting GearSet to subclasses."""

    __parent__: "GearSet"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2676.SpecialisedAssembly":
        return self.__parent__._cast(_2676.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2629.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2629

        return self.__parent__._cast(_2629.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2716.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2716

        return self.__parent__._cast(_2716.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2718.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2718

        return self.__parent__._cast(_2718.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2722.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2722

        return self.__parent__._cast(_2722.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2724.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2724

        return self.__parent__._cast(_2724.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2726.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2726

        return self.__parent__._cast(_2726.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2728.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2728

        return self.__parent__._cast(_2728.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2731.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2731

        return self.__parent__._cast(_2731.FaceGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2737.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2737

        return self.__parent__._cast(_2737.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2739.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2739

        return self.__parent__._cast(_2739.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2741.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2741

        return self.__parent__._cast(_2741.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2743.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2743

        return self.__parent__._cast(_2743.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2744.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2744

        return self.__parent__._cast(_2744.PlanetaryGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2747.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2747

        return self.__parent__._cast(_2747.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2749.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2749

        return self.__parent__._cast(_2749.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2751.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2755.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2757.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.ZerolBevelGearSet)

    @property
    def gear_set(self: "CastSelf") -> "GearSet":
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
class GearSet(_2676.SpecialisedAssembly):
    """GearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_design(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_GearSetDesign":
        """ListWithSelectedItem[mastapy.gears.gear_designs.GearSetDesign]"""
        temp = pythonnet_property_get(self.wrapped, "ActiveDesign")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_GearSetDesign",
        )(temp)

    @active_design.setter
    @enforce_parameter_types
    def active_design(self: "Self", value: "_1047.GearSetDesign") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_GearSetDesign.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_GearSetDesign.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ActiveDesign", value)

    @property
    def maximum_number_of_teeth_in_mesh(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeethInMesh")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth_in_mesh.setter
    @enforce_parameter_types
    def maximum_number_of_teeth_in_mesh(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfTeethInMesh",
            int(value) if value is not None else 0,
        )

    @property
    def mesh_ratio_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeshRatioLimit")

        if temp is None:
            return 0.0

        return temp

    @mesh_ratio_limit.setter
    @enforce_parameter_types
    def mesh_ratio_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeshRatioLimit", float(value) if value is not None else 0.0
        )

    @property
    def minimum_number_of_teeth_in_mesh(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeethInMesh")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth_in_mesh.setter
    @enforce_parameter_types
    def minimum_number_of_teeth_in_mesh(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfTeethInMesh",
            int(value) if value is not None else 0,
        )

    @property
    def required_safety_factor_for_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RequiredSafetyFactorForBending", value)

    @property
    def required_safety_factor_for_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RequiredSafetyFactorForContact", value)

    @property
    def required_safety_factor_for_static_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticBending"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_static_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RequiredSafetyFactorForStaticBending", value
        )

    @property
    def required_safety_factor_for_static_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticContact"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_static_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RequiredSafetyFactorForStaticContact", value
        )

    @property
    def active_gear_set_design(self: "Self") -> "_1047.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set_designs(self: "Self") -> "List[_1047.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def add_gear_set_design(self: "Self", design: "_1047.GearSetDesign") -> None:
        """Method does not return.

        Args:
            design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped, "AddGearSetDesign", design.wrapped if design else None
        )

    @enforce_parameter_types
    def remove_design(self: "Self", design: "_1047.GearSetDesign") -> None:
        """Method does not return.

        Args:
            design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveDesign", design.wrapped if design else None
        )

    @enforce_parameter_types
    def set_active_gear_set_design(
        self: "Self", gear_set_design: "_1047.GearSetDesign"
    ) -> None:
        """Method does not return.

        Args:
            gear_set_design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetActiveGearSetDesign",
            gear_set_design.wrapped if gear_set_design else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSet":
        """Cast to another type.

        Returns:
            _Cast_GearSet
        """
        return _Cast_GearSet(self)
