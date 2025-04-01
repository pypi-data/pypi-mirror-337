"""MeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1335

_MESH_LOAD_CASE = python_net_import("SMT.MastaAPI.Gears.LoadCase", "MeshLoadCase")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1329
    from mastapy._private.gears.load_case.bevel import _988
    from mastapy._private.gears.load_case.concept import _986
    from mastapy._private.gears.load_case.conical import _983
    from mastapy._private.gears.load_case.cylindrical import _980
    from mastapy._private.gears.load_case.face import _977
    from mastapy._private.gears.load_case.worm import _974

    Self = TypeVar("Self", bound="MeshLoadCase")
    CastSelf = TypeVar("CastSelf", bound="MeshLoadCase._Cast_MeshLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("MeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshLoadCase:
    """Special nested class for casting MeshLoadCase to subclasses."""

    __parent__: "MeshLoadCase"

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1335.GearMeshDesignAnalysis":
        return self.__parent__._cast(_1335.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1329.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1329

        return self.__parent__._cast(_1329.AbstractGearMeshAnalysis)

    @property
    def worm_mesh_load_case(self: "CastSelf") -> "_974.WormMeshLoadCase":
        from mastapy._private.gears.load_case.worm import _974

        return self.__parent__._cast(_974.WormMeshLoadCase)

    @property
    def face_mesh_load_case(self: "CastSelf") -> "_977.FaceMeshLoadCase":
        from mastapy._private.gears.load_case.face import _977

        return self.__parent__._cast(_977.FaceMeshLoadCase)

    @property
    def cylindrical_mesh_load_case(self: "CastSelf") -> "_980.CylindricalMeshLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _980

        return self.__parent__._cast(_980.CylindricalMeshLoadCase)

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "_983.ConicalMeshLoadCase":
        from mastapy._private.gears.load_case.conical import _983

        return self.__parent__._cast(_983.ConicalMeshLoadCase)

    @property
    def concept_mesh_load_case(self: "CastSelf") -> "_986.ConceptMeshLoadCase":
        from mastapy._private.gears.load_case.concept import _986

        return self.__parent__._cast(_986.ConceptMeshLoadCase)

    @property
    def bevel_mesh_load_case(self: "CastSelf") -> "_988.BevelMeshLoadCase":
        from mastapy._private.gears.load_case.bevel import _988

        return self.__parent__._cast(_988.BevelMeshLoadCase)

    @property
    def mesh_load_case(self: "CastSelf") -> "MeshLoadCase":
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
class MeshLoadCase(_1335.GearMeshDesignAnalysis):
    """MeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def driving_gear(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DrivingGear")

        if temp is None:
            return ""

        return temp

    @property
    def driving_gear_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DrivingGearPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_a_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearATorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_b_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def is_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoaded")

        if temp is None:
            return False

        return temp

    @property
    def signed_gear_a_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearAPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_gear_a_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearATorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_gear_b_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearBPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_gear_b_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedGearBTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_MeshLoadCase
        """
        return _Cast_MeshLoadCase(self)
