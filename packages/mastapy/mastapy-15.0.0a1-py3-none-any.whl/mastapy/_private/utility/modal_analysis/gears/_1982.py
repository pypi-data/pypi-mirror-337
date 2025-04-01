"""OrderForTE"""

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

_ORDER_FOR_TE = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "OrderForTE"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.modal_analysis.gears import (
        _1977,
        _1978,
        _1980,
        _1981,
        _1983,
        _1984,
        _1985,
        _1986,
        _1987,
    )

    Self = TypeVar("Self", bound="OrderForTE")
    CastSelf = TypeVar("CastSelf", bound="OrderForTE._Cast_OrderForTE")


__docformat__ = "restructuredtext en"
__all__ = ("OrderForTE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OrderForTE:
    """Special nested class for casting OrderForTE to subclasses."""

    __parent__: "OrderForTE"

    @property
    def gear_mesh_for_te(self: "CastSelf") -> "_1977.GearMeshForTE":
        from mastapy._private.utility.modal_analysis.gears import _1977

        return self.__parent__._cast(_1977.GearMeshForTE)

    @property
    def gear_order_for_te(self: "CastSelf") -> "_1978.GearOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1978

        return self.__parent__._cast(_1978.GearOrderForTE)

    @property
    def harmonic_order_for_te(self: "CastSelf") -> "_1980.HarmonicOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1980

        return self.__parent__._cast(_1980.HarmonicOrderForTE)

    @property
    def label_only_order(self: "CastSelf") -> "_1981.LabelOnlyOrder":
        from mastapy._private.utility.modal_analysis.gears import _1981

        return self.__parent__._cast(_1981.LabelOnlyOrder)

    @property
    def order_selector(self: "CastSelf") -> "_1983.OrderSelector":
        from mastapy._private.utility.modal_analysis.gears import _1983

        return self.__parent__._cast(_1983.OrderSelector)

    @property
    def order_with_radius(self: "CastSelf") -> "_1984.OrderWithRadius":
        from mastapy._private.utility.modal_analysis.gears import _1984

        return self.__parent__._cast(_1984.OrderWithRadius)

    @property
    def rolling_bearing_order(self: "CastSelf") -> "_1985.RollingBearingOrder":
        from mastapy._private.utility.modal_analysis.gears import _1985

        return self.__parent__._cast(_1985.RollingBearingOrder)

    @property
    def shaft_order_for_te(self: "CastSelf") -> "_1986.ShaftOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1986

        return self.__parent__._cast(_1986.ShaftOrderForTE)

    @property
    def user_defined_order_for_te(self: "CastSelf") -> "_1987.UserDefinedOrderForTE":
        from mastapy._private.utility.modal_analysis.gears import _1987

        return self.__parent__._cast(_1987.UserDefinedOrderForTE)

    @property
    def order_for_te(self: "CastSelf") -> "OrderForTE":
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
class OrderForTE(_0.APIBase):
    """OrderForTE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ORDER_FOR_TE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def frequency_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FrequencyOffset")

        if temp is None:
            return 0.0

        return temp

    @frequency_offset.setter
    @enforce_parameter_types
    def frequency_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FrequencyOffset", float(value) if value is not None else 0.0
        )

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
    def order(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Order")

        if temp is None:
            return 0.0

        return temp

    @property
    def children(self: "Self") -> "List[OrderForTE]":
        """List[mastapy.utility.modal_analysis.gears.OrderForTE]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Children")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

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
    def cast_to(self: "Self") -> "_Cast_OrderForTE":
        """Cast to another type.

        Returns:
            _Cast_OrderForTE
        """
        return _Cast_OrderForTE(self)
