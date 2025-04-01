"""ConicalRateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _451

_CONICAL_RATEABLE_MESH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalRateableMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.agma_gleason_conical import _652
    from mastapy._private.gears.rating.bevel.standards import _648
    from mastapy._private.gears.rating.hypoid.standards import _528
    from mastapy._private.gears.rating.iso_10300 import _511

    Self = TypeVar("Self", bound="ConicalRateableMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalRateableMesh._Cast_ConicalRateableMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalRateableMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalRateableMesh:
    """Special nested class for casting ConicalRateableMesh to subclasses."""

    __parent__: "ConicalRateableMesh"

    @property
    def rateable_mesh(self: "CastSelf") -> "_451.RateableMesh":
        return self.__parent__._cast(_451.RateableMesh)

    @property
    def iso10300_rateable_mesh(self: "CastSelf") -> "_511.ISO10300RateableMesh":
        from mastapy._private.gears.rating.iso_10300 import _511

        return self.__parent__._cast(_511.ISO10300RateableMesh)

    @property
    def hypoid_rateable_mesh(self: "CastSelf") -> "_528.HypoidRateableMesh":
        from mastapy._private.gears.rating.hypoid.standards import _528

        return self.__parent__._cast(_528.HypoidRateableMesh)

    @property
    def spiral_bevel_rateable_mesh(self: "CastSelf") -> "_648.SpiralBevelRateableMesh":
        from mastapy._private.gears.rating.bevel.standards import _648

        return self.__parent__._cast(_648.SpiralBevelRateableMesh)

    @property
    def agma_gleason_conical_rateable_mesh(
        self: "CastSelf",
    ) -> "_652.AGMAGleasonConicalRateableMesh":
        from mastapy._private.gears.rating.agma_gleason_conical import _652

        return self.__parent__._cast(_652.AGMAGleasonConicalRateableMesh)

    @property
    def conical_rateable_mesh(self: "CastSelf") -> "ConicalRateableMesh":
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
class ConicalRateableMesh(_451.RateableMesh):
    """ConicalRateableMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_RATEABLE_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalRateableMesh":
        """Cast to another type.

        Returns:
            _Cast_ConicalRateableMesh
        """
        return _Cast_ConicalRateableMesh(self)
