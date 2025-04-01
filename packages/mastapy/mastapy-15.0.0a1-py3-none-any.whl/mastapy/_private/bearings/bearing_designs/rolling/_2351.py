"""NonBarrelRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.bearings.bearing_designs.rolling import _2352

_NON_BARREL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "NonBarrelRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2320, _2321, _2324
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2328,
        _2329,
        _2339,
        _2350,
        _2353,
        _2354,
        _2355,
        _2362,
    )

    Self = TypeVar("Self", bound="NonBarrelRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="NonBarrelRollerBearing._Cast_NonBarrelRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NonBarrelRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonBarrelRollerBearing:
    """Special nested class for casting NonBarrelRollerBearing to subclasses."""

    __parent__: "NonBarrelRollerBearing"

    @property
    def roller_bearing(self: "CastSelf") -> "_2352.RollerBearing":
        return self.__parent__._cast(_2352.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2355.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2355

        return self.__parent__._cast(_2355.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2321.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2321

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
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2339.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2339

        return self.__parent__._cast(_2339.CylindricalRollerBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2350.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2350

        return self.__parent__._cast(_2350.NeedleRollerBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2362.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2362

        return self.__parent__._cast(_2362.TaperRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "NonBarrelRollerBearing":
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
class NonBarrelRollerBearing(_2352.RollerBearing):
    """NonBarrelRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_BARREL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def roller_end_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RollerEndRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @roller_end_radius.setter
    @enforce_parameter_types
    def roller_end_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RollerEndRadius", value)

    @property
    def roller_end_shape(self: "Self") -> "_2353.RollerEndShape":
        """mastapy.bearings.bearing_designs.rolling.RollerEndShape"""
        temp = pythonnet_property_get(self.wrapped, "RollerEndShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.RollerEndShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2353", "RollerEndShape"
        )(value)

    @roller_end_shape.setter
    @enforce_parameter_types
    def roller_end_shape(self: "Self", value: "_2353.RollerEndShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.RollerEndShape"
        )
        pythonnet_property_set(self.wrapped, "RollerEndShape", value)

    @property
    def ribs(self: "Self") -> "List[_2354.RollerRibDetail]":
        """List[mastapy.bearings.bearing_designs.rolling.RollerRibDetail]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ribs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NonBarrelRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_NonBarrelRollerBearing
        """
        return _Cast_NonBarrelRollerBearing(self)
