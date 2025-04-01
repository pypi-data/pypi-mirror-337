"""GenericConvectionFace"""

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
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _180

_GENERIC_CONVECTION_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "GenericConvectionFace"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _181,
        _213,
    )

    Self = TypeVar("Self", bound="GenericConvectionFace")
    CastSelf = TypeVar(
        "CastSelf", bound="GenericConvectionFace._Cast_GenericConvectionFace"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GenericConvectionFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GenericConvectionFace:
    """Special nested class for casting GenericConvectionFace to subclasses."""

    __parent__: "GenericConvectionFace"

    @property
    def convection_face(self: "CastSelf") -> "_180.ConvectionFace":
        return self.__parent__._cast(_180.ConvectionFace)

    @property
    def convection_face_base(self: "CastSelf") -> "_181.ConvectionFaceBase":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _181,
        )

        return self.__parent__._cast(_181.ConvectionFaceBase)

    @property
    def thermal_face(self: "CastSelf") -> "_213.ThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _213,
        )

        return self.__parent__._cast(_213.ThermalFace)

    @property
    def generic_convection_face(self: "CastSelf") -> "GenericConvectionFace":
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
class GenericConvectionFace(_180.ConvectionFace):
    """GenericConvectionFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERIC_CONVECTION_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def area_modification_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AreaModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @area_modification_factor.setter
    @enforce_parameter_types
    def area_modification_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AreaModificationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def modified_surface_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedSurfaceArea")

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
    def surface_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceArea")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GenericConvectionFace":
        """Cast to another type.

        Returns:
            _Cast_GenericConvectionFace
        """
        return _Cast_GenericConvectionFace(self)
