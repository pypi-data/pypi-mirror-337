"""CouplingHalf"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2662

_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2394
    from mastapy._private.system_model.part_model import _2639, _2666
    from mastapy._private.system_model.part_model.couplings import (
        _2783,
        _2786,
        _2792,
        _2794,
        _2796,
        _2803,
        _2812,
        _2815,
        _2816,
        _2817,
        _2819,
        _2821,
    )

    Self = TypeVar("Self", bound="CouplingHalf")
    CastSelf = TypeVar("CastSelf", bound="CouplingHalf._Cast_CouplingHalf")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalf:
    """Special nested class for casting CouplingHalf to subclasses."""

    __parent__: "CouplingHalf"

    @property
    def mountable_component(self: "CastSelf") -> "_2662.MountableComponent":
        return self.__parent__._cast(_2662.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2639.Component":
        from mastapy._private.system_model.part_model import _2639

        return self.__parent__._cast(_2639.Component)

    @property
    def part(self: "CastSelf") -> "_2666.Part":
        from mastapy._private.system_model.part_model import _2666

        return self.__parent__._cast(_2666.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2394.DesignEntity":
        from mastapy._private.system_model import _2394

        return self.__parent__._cast(_2394.DesignEntity)

    @property
    def clutch_half(self: "CastSelf") -> "_2783.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2783

        return self.__parent__._cast(_2783.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2786.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2786

        return self.__parent__._cast(_2786.ConceptCouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2792.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2792

        return self.__parent__._cast(_2792.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2794.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2794

        return self.__parent__._cast(_2794.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2796.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2796

        return self.__parent__._cast(_2796.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2803.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2803

        return self.__parent__._cast(_2803.RollingRing)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2812.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2812

        return self.__parent__._cast(_2812.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2815.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2815

        return self.__parent__._cast(_2815.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2816.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2816

        return self.__parent__._cast(_2816.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2817.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2817

        return self.__parent__._cast(_2817.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2819.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2819

        return self.__parent__._cast(_2819.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2821.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.TorqueConverterTurbine)

    @property
    def coupling_half(self: "CastSelf") -> "CouplingHalf":
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
class CouplingHalf(_2662.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore.setter
    @enforce_parameter_types
    def bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bore", value)

    @property
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalf
        """
        return _Cast_CouplingHalf(self)
