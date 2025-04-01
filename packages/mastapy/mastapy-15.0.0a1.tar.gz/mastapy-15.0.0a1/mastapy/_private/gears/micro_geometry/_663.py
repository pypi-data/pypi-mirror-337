"""Modification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MODIFICATION = python_net_import("SMT.MastaAPI.Gears.MicroGeometry", "Modification")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical.micro_geometry import (
        _1285,
        _1287,
        _1288,
    )
    from mastapy._private.gears.gear_designs.cylindrical import _1125
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1199,
        _1202,
        _1203,
        _1211,
        _1212,
        _1216,
    )
    from mastapy._private.gears.micro_geometry import _653, _656, _666

    Self = TypeVar("Self", bound="Modification")
    CastSelf = TypeVar("CastSelf", bound="Modification._Cast_Modification")


__docformat__ = "restructuredtext en"
__all__ = ("Modification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Modification:
    """Special nested class for casting Modification to subclasses."""

    __parent__: "Modification"

    @property
    def bias_modification(self: "CastSelf") -> "_653.BiasModification":
        from mastapy._private.gears.micro_geometry import _653

        return self.__parent__._cast(_653.BiasModification)

    @property
    def lead_modification(self: "CastSelf") -> "_656.LeadModification":
        from mastapy._private.gears.micro_geometry import _656

        return self.__parent__._cast(_656.LeadModification)

    @property
    def profile_modification(self: "CastSelf") -> "_666.ProfileModification":
        from mastapy._private.gears.micro_geometry import _666

        return self.__parent__._cast(_666.ProfileModification)

    @property
    def cylindrical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1199.CylindricalGearBiasModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1199

        return self.__parent__._cast(_1199.CylindricalGearBiasModification)

    @property
    def cylindrical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1202.CylindricalGearLeadModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1202

        return self.__parent__._cast(_1202.CylindricalGearLeadModification)

    @property
    def cylindrical_gear_lead_modification_at_profile_position(
        self: "CastSelf",
    ) -> "_1203.CylindricalGearLeadModificationAtProfilePosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1203

        return self.__parent__._cast(
            _1203.CylindricalGearLeadModificationAtProfilePosition
        )

    @property
    def cylindrical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1211.CylindricalGearProfileModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1211

        return self.__parent__._cast(_1211.CylindricalGearProfileModification)

    @property
    def cylindrical_gear_profile_modification_at_face_width_position(
        self: "CastSelf",
    ) -> "_1212.CylindricalGearProfileModificationAtFaceWidthPosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1212

        return self.__parent__._cast(
            _1212.CylindricalGearProfileModificationAtFaceWidthPosition
        )

    @property
    def cylindrical_gear_triangular_end_modification(
        self: "CastSelf",
    ) -> "_1216.CylindricalGearTriangularEndModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1216

        return self.__parent__._cast(_1216.CylindricalGearTriangularEndModification)

    @property
    def conical_gear_bias_modification(
        self: "CastSelf",
    ) -> "_1285.ConicalGearBiasModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1285

        return self.__parent__._cast(_1285.ConicalGearBiasModification)

    @property
    def conical_gear_lead_modification(
        self: "CastSelf",
    ) -> "_1287.ConicalGearLeadModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1287

        return self.__parent__._cast(_1287.ConicalGearLeadModification)

    @property
    def conical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1288.ConicalGearProfileModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1288

        return self.__parent__._cast(_1288.ConicalGearProfileModification)

    @property
    def modification(self: "CastSelf") -> "Modification":
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
class Modification(_0.APIBase):
    """Modification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def settings(self: "Self") -> "_1125.CylindricalGearMicroGeometrySettingsItem":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Modification":
        """Cast to another type.

        Returns:
            _Cast_Modification
        """
        return _Cast_Modification(self)
