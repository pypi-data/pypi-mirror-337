"""HobbingProcessCalculation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _776,
)

_HOBBING_PROCESS_CALCULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "HobbingProcessCalculation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _763,
        _764,
        _765,
        _766,
        _767,
        _771,
    )

    Self = TypeVar("Self", bound="HobbingProcessCalculation")
    CastSelf = TypeVar(
        "CastSelf", bound="HobbingProcessCalculation._Cast_HobbingProcessCalculation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HobbingProcessCalculation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HobbingProcessCalculation:
    """Special nested class for casting HobbingProcessCalculation to subclasses."""

    __parent__: "HobbingProcessCalculation"

    @property
    def process_calculation(self: "CastSelf") -> "_776.ProcessCalculation":
        return self.__parent__._cast(_776.ProcessCalculation)

    @property
    def hobbing_process_gear_shape(self: "CastSelf") -> "_763.HobbingProcessGearShape":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _763,
        )

        return self.__parent__._cast(_763.HobbingProcessGearShape)

    @property
    def hobbing_process_lead_calculation(
        self: "CastSelf",
    ) -> "_764.HobbingProcessLeadCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _764,
        )

        return self.__parent__._cast(_764.HobbingProcessLeadCalculation)

    @property
    def hobbing_process_mark_on_shaft(
        self: "CastSelf",
    ) -> "_765.HobbingProcessMarkOnShaft":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _765,
        )

        return self.__parent__._cast(_765.HobbingProcessMarkOnShaft)

    @property
    def hobbing_process_pitch_calculation(
        self: "CastSelf",
    ) -> "_766.HobbingProcessPitchCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _766,
        )

        return self.__parent__._cast(_766.HobbingProcessPitchCalculation)

    @property
    def hobbing_process_profile_calculation(
        self: "CastSelf",
    ) -> "_767.HobbingProcessProfileCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _767,
        )

        return self.__parent__._cast(_767.HobbingProcessProfileCalculation)

    @property
    def hobbing_process_total_modification_calculation(
        self: "CastSelf",
    ) -> "_771.HobbingProcessTotalModificationCalculation":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _771,
        )

        return self.__parent__._cast(_771.HobbingProcessTotalModificationCalculation)

    @property
    def hobbing_process_calculation(self: "CastSelf") -> "HobbingProcessCalculation":
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
class HobbingProcessCalculation(_776.ProcessCalculation):
    """HobbingProcessCalculation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOBBING_PROCESS_CALCULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_HobbingProcessCalculation":
        """Cast to another type.

        Returns:
            _Cast_HobbingProcessCalculation
        """
        return _Cast_HobbingProcessCalculation(self)
