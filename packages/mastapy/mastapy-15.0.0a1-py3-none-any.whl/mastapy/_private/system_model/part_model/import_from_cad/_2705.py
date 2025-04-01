"""MountableComponentFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2695

_MOUNTABLE_COMPONENT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "MountableComponentFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2694,
        _2696,
        _2697,
        _2698,
        _2699,
        _2700,
        _2701,
        _2702,
        _2703,
        _2707,
        _2708,
        _2709,
    )

    Self = TypeVar("Self", bound="MountableComponentFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="MountableComponentFromCAD._Cast_MountableComponentFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentFromCAD:
    """Special nested class for casting MountableComponentFromCAD to subclasses."""

    __parent__: "MountableComponentFromCAD"

    @property
    def component_from_cad(self: "CastSelf") -> "_2695.ComponentFromCAD":
        return self.__parent__._cast(_2695.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2696.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2696

        return self.__parent__._cast(_2696.ComponentFromCADBase)

    @property
    def clutch_from_cad(self: "CastSelf") -> "_2694.ClutchFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2694

        return self.__parent__._cast(_2694.ClutchFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "_2697.ConceptBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2697

        return self.__parent__._cast(_2697.ConceptBearingFromCAD)

    @property
    def connector_from_cad(self: "CastSelf") -> "_2698.ConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2698

        return self.__parent__._cast(_2698.ConnectorFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2699.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2699

        return self.__parent__._cast(_2699.CylindricalGearFromCAD)

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2700.CylindricalGearInPlanetarySetFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2700

        return self.__parent__._cast(_2700.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "_2701.CylindricalPlanetGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2701

        return self.__parent__._cast(_2701.CylindricalPlanetGearFromCAD)

    @property
    def cylindrical_ring_gear_from_cad(
        self: "CastSelf",
    ) -> "_2702.CylindricalRingGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2702

        return self.__parent__._cast(_2702.CylindricalRingGearFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(
        self: "CastSelf",
    ) -> "_2703.CylindricalSunGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2703

        return self.__parent__._cast(_2703.CylindricalSunGearFromCAD)

    @property
    def pulley_from_cad(self: "CastSelf") -> "_2707.PulleyFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2707

        return self.__parent__._cast(_2707.PulleyFromCAD)

    @property
    def rigid_connector_from_cad(self: "CastSelf") -> "_2708.RigidConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2708

        return self.__parent__._cast(_2708.RigidConnectorFromCAD)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "_2709.RollingBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2709

        return self.__parent__._cast(_2709.RollingBearingFromCAD)

    @property
    def mountable_component_from_cad(self: "CastSelf") -> "MountableComponentFromCAD":
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
class MountableComponentFromCAD(_2695.ComponentFromCAD):
    """MountableComponentFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentFromCAD":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentFromCAD
        """
        return _Cast_MountableComponentFromCAD(self)
