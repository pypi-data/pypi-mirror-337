"""NonCADElectricMachineDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines import _1380

_NON_CAD_ELECTRIC_MACHINE_DETAIL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "NonCADElectricMachineDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import (
        _1379,
        _1403,
        _1417,
        _1428,
        _1432,
        _1434,
        _1451,
    )

    Self = TypeVar("Self", bound="NonCADElectricMachineDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NonCADElectricMachineDetail._Cast_NonCADElectricMachineDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NonCADElectricMachineDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonCADElectricMachineDetail:
    """Special nested class for casting NonCADElectricMachineDetail to subclasses."""

    __parent__: "NonCADElectricMachineDetail"

    @property
    def electric_machine_detail(self: "CastSelf") -> "_1380.ElectricMachineDetail":
        return self.__parent__._cast(_1380.ElectricMachineDetail)

    @property
    def electric_machine_design_base(
        self: "CastSelf",
    ) -> "_1379.ElectricMachineDesignBase":
        from mastapy._private.electric_machines import _1379

        return self.__parent__._cast(_1379.ElectricMachineDesignBase)

    @property
    def interior_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1403.InteriorPermanentMagnetMachine":
        from mastapy._private.electric_machines import _1403

        return self.__parent__._cast(_1403.InteriorPermanentMagnetMachine)

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
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "NonCADElectricMachineDetail":
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
class NonCADElectricMachineDetail(_1380.ElectricMachineDetail):
    """NonCADElectricMachineDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_CAD_ELECTRIC_MACHINE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def stator(self: "Self") -> "_1428.Stator":
        """mastapy.electric_machines.Stator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_NonCADElectricMachineDetail":
        """Cast to another type.

        Returns:
            _Cast_NonCADElectricMachineDetail
        """
        return _Cast_NonCADElectricMachineDetail(self)
