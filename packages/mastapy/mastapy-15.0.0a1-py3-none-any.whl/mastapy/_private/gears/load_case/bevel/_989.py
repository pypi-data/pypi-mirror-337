"""BevelSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case.conical import _982

_BEVEL_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Bevel", "BevelSetLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1330, _1339
    from mastapy._private.gears.load_case import _970

    Self = TypeVar("Self", bound="BevelSetLoadCase")
    CastSelf = TypeVar("CastSelf", bound="BevelSetLoadCase._Cast_BevelSetLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("BevelSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelSetLoadCase:
    """Special nested class for casting BevelSetLoadCase to subclasses."""

    __parent__: "BevelSetLoadCase"

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_982.ConicalGearSetLoadCase":
        return self.__parent__._cast(_982.ConicalGearSetLoadCase)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_970.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _970

        return self.__parent__._cast(_970.GearSetLoadCaseBase)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1339.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1339

        return self.__parent__._cast(_1339.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1330.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1330

        return self.__parent__._cast(_1330.AbstractGearSetAnalysis)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "BevelSetLoadCase":
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
class BevelSetLoadCase(_982.ConicalGearSetLoadCase):
    """BevelSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BevelSetLoadCase
        """
        return _Cast_BevelSetLoadCase(self)
