"""UserDefinedNodeInformation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_USER_DEFINED_NODE_INFORMATION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "UserDefinedNodeInformation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _203

    Self = TypeVar("Self", bound="UserDefinedNodeInformation")
    CastSelf = TypeVar(
        "CastSelf", bound="UserDefinedNodeInformation._Cast_UserDefinedNodeInformation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserDefinedNodeInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserDefinedNodeInformation:
    """Special nested class for casting UserDefinedNodeInformation to subclasses."""

    __parent__: "UserDefinedNodeInformation"

    @property
    def user_defined_node_information(self: "CastSelf") -> "UserDefinedNodeInformation":
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
class UserDefinedNodeInformation(_0.APIBase):
    """UserDefinedNodeInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_DEFINED_NODE_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def x_location(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XLocation")

        if temp is None:
            return 0.0

        return temp

    @x_location.setter
    @enforce_parameter_types
    def x_location(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XLocation", float(value) if value is not None else 0.0
        )

    @property
    def y_location(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YLocation")

        if temp is None:
            return 0.0

        return temp

    @y_location.setter
    @enforce_parameter_types
    def y_location(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YLocation", float(value) if value is not None else 0.0
        )

    @property
    def nodes_to_connect_to(
        self: "Self",
    ) -> "List[_203.NodeConnectedToUserDefinedNode]":
        """List[mastapy.nodal_analysis.lumped_parameter_thermal_analysis.NodeConnectedToUserDefinedNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodesToConnectTo")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def nodes_available_for_connection(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodesAvailableForConnection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

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

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def set_nodes_to_connect_to(
        self: "Self", nodes: "List[_203.NodeConnectedToUserDefinedNode]"
    ) -> None:
        """Method does not return.

        Args:
            nodes (List[mastapy.nodal_analysis.lumped_parameter_thermal_analysis.NodeConnectedToUserDefinedNode])
        """
        nodes = conversion.mp_to_pn_objects_in_dotnet_list(nodes)
        pythonnet_method_call(self.wrapped, "SetNodesToConnectTo", nodes)

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
    def cast_to(self: "Self") -> "_Cast_UserDefinedNodeInformation":
        """Cast to another type.

        Returns:
            _Cast_UserDefinedNodeInformation
        """
        return _Cast_UserDefinedNodeInformation(self)
