"""RotorSetup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.thermal import _1455

_ROTOR_SETUP = python_net_import("SMT.MastaAPI.ElectricMachines.Thermal", "RotorSetup")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="RotorSetup")
    CastSelf = TypeVar("CastSelf", bound="RotorSetup._Cast_RotorSetup")


__docformat__ = "restructuredtext en"
__all__ = ("RotorSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorSetup:
    """Special nested class for casting RotorSetup to subclasses."""

    __parent__: "RotorSetup"

    @property
    def component_setup(self: "CastSelf") -> "_1455.ComponentSetup":
        return self.__parent__._cast(_1455.ComponentSetup)

    @property
    def rotor_setup(self: "CastSelf") -> "RotorSetup":
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
class RotorSetup(_1455.ComponentSetup):
    """RotorSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def specify_edge_indices_for_rotor_outer_boundary(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyEdgeIndicesForRotorOuterBoundary"
        )

        if temp is None:
            return False

        return temp

    @specify_edge_indices_for_rotor_outer_boundary.setter
    @enforce_parameter_types
    def specify_edge_indices_for_rotor_outer_boundary(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyEdgeIndicesForRotorOuterBoundary",
            bool(value) if value is not None else False,
        )

    @property
    def number_of_rotor_edges(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRotorEdges")

        if temp is None:
            return 0

        return temp

    @property
    def selected_edge_indices(self: "Self") -> "List[int]":
        """List[int]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    def set_edge_indices(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetEdgeIndices")

    @enforce_parameter_types
    def set_selected_edge_indices(
        self: "Self", zero_based_edge_indices: "List[int]"
    ) -> None:
        """Method does not return.

        Args:
            zero_based_edge_indices (List[int])
        """
        zero_based_edge_indices = conversion.mp_to_pn_objects_in_list(
            zero_based_edge_indices
        )
        pythonnet_method_call(
            self.wrapped, "SetSelectedEdgeIndices", zero_based_edge_indices
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RotorSetup":
        """Cast to another type.

        Returns:
            _Cast_RotorSetup
        """
        return _Cast_RotorSetup(self)
