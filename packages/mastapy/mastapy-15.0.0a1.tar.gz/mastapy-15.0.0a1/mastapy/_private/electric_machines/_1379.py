"""ElectricMachineDesignBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1388

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ELECTRIC_MACHINE_DESIGN_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineDesignBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import (
        _1361,
        _1380,
        _1403,
        _1414,
        _1417,
        _1432,
        _1434,
        _1451,
    )
    from mastapy._private.electric_machines.thermal import _1471

    Self = TypeVar("Self", bound="ElectricMachineDesignBase")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineDesignBase._Cast_ElectricMachineDesignBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDesignBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDesignBase:
    """Special nested class for casting ElectricMachineDesignBase to subclasses."""

    __parent__: "ElectricMachineDesignBase"

    @property
    def cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1361.CADElectricMachineDetail":
        from mastapy._private.electric_machines import _1361

        return self.__parent__._cast(_1361.CADElectricMachineDetail)

    @property
    def electric_machine_detail(self: "CastSelf") -> "_1380.ElectricMachineDetail":
        from mastapy._private.electric_machines import _1380

        return self.__parent__._cast(_1380.ElectricMachineDetail)

    @property
    def interior_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1403.InteriorPermanentMagnetMachine":
        from mastapy._private.electric_machines import _1403

        return self.__parent__._cast(_1403.InteriorPermanentMagnetMachine)

    @property
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1414.NonCADElectricMachineDetail":
        from mastapy._private.electric_machines import _1414

        return self.__parent__._cast(_1414.NonCADElectricMachineDetail)

    @property
    def permanent_magnet_assisted_synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1417.PermanentMagnetAssistedSynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1417

        return self.__parent__._cast(
            _1417.PermanentMagnetAssistedSynchronousReluctanceMachine
        )

    @property
    def surface_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1432.SurfacePermanentMagnetMachine":
        from mastapy._private.electric_machines import _1432

        return self.__parent__._cast(_1432.SurfacePermanentMagnetMachine)

    @property
    def synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1434.SynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1434

        return self.__parent__._cast(_1434.SynchronousReluctanceMachine)

    @property
    def wound_field_synchronous_machine(
        self: "CastSelf",
    ) -> "_1451.WoundFieldSynchronousMachine":
        from mastapy._private.electric_machines import _1451

        return self.__parent__._cast(_1451.WoundFieldSynchronousMachine)

    @property
    def thermal_electric_machine(self: "CastSelf") -> "_1471.ThermalElectricMachine":
        from mastapy._private.electric_machines.thermal import _1471

        return self.__parent__._cast(_1471.ThermalElectricMachine)

    @property
    def electric_machine_design_base(self: "CastSelf") -> "ElectricMachineDesignBase":
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
class ElectricMachineDesignBase(_0.APIBase):
    """ElectricMachineDesignBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DESIGN_BASE

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
    def select_setup(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineSetupBase":
        """ListWithSelectedItem[mastapy.electric_machines.ElectricMachineSetupBase]"""
        temp = pythonnet_property_get(self.wrapped, "SelectSetup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineSetupBase",
        )(temp)

    @select_setup.setter
    @enforce_parameter_types
    def select_setup(self: "Self", value: "_1388.ElectricMachineSetupBase") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineSetupBase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineSetupBase.implicit_type()
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "SelectSetup", value)

    @property
    def shaft_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ShaftMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @shaft_material_database.setter
    @enforce_parameter_types
    def shaft_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ShaftMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

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
    def remove_setup(self: "Self", setup: "_1388.ElectricMachineSetupBase") -> None:
        """Method does not return.

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetupBase)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveSetup", setup.wrapped if setup else None
        )

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDesignBase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDesignBase
        """
        return _Cast_ElectricMachineDesignBase(self)
