"""CylindricalGearMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _353

_CYLINDRICAL_GEAR_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "CylindricalGearMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.materials import _675, _676, _677, _679
    from mastapy._private.utility.databases import _2006, _2010, _2014

    Self = TypeVar("Self", bound="CylindricalGearMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMaterialDatabase._Cast_CylindricalGearMaterialDatabase",
    )

T = TypeVar("T", bound="_677.CylindricalGearMaterial")

__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMaterialDatabase:
    """Special nested class for casting CylindricalGearMaterialDatabase to subclasses."""

    __parent__: "CylindricalGearMaterialDatabase"

    @property
    def material_database(self: "CastSelf") -> "_353.MaterialDatabase":
        return self.__parent__._cast(_353.MaterialDatabase)

    @property
    def named_database(self: "CastSelf") -> "_2010.NamedDatabase":
        from mastapy._private.utility.databases import _2010

        return self.__parent__._cast(_2010.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_2014.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _2014

        return self.__parent__._cast(_2014.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2006.Database":
        pass

        from mastapy._private.utility.databases import _2006

        return self.__parent__._cast(_2006.Database)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_675.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _675

        return self.__parent__._cast(_675.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_676.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _676

        return self.__parent__._cast(_676.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_679.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _679

        return self.__parent__._cast(_679.CylindricalGearPlasticMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "CylindricalGearMaterialDatabase":
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
class CylindricalGearMaterialDatabase(_353.MaterialDatabase[T]):
    """CylindricalGearMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMaterialDatabase
        """
        return _Cast_CylindricalGearMaterialDatabase(self)
