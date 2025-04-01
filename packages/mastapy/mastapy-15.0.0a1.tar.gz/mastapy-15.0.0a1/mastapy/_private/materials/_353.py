"""MaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _2010

_MATERIAL_DATABASE = python_net_import("SMT.MastaAPI.Materials", "MaterialDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.cycloidal import _1633, _1640
    from mastapy._private.electric_machines import _1398, _1412, _1431, _1446
    from mastapy._private.gears.materials import _669, _671, _675, _676, _678, _679
    from mastapy._private.materials import _352
    from mastapy._private.shafts import _25
    from mastapy._private.utility.databases import _2006, _2014

    Self = TypeVar("Self", bound="MaterialDatabase")
    CastSelf = TypeVar("CastSelf", bound="MaterialDatabase._Cast_MaterialDatabase")

T = TypeVar("T", bound="_352.Material")

__docformat__ = "restructuredtext en"
__all__ = ("MaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialDatabase:
    """Special nested class for casting MaterialDatabase to subclasses."""

    __parent__: "MaterialDatabase"

    @property
    def named_database(self: "CastSelf") -> "_2010.NamedDatabase":
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
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_669.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _669

        return self.__parent__._cast(_669.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_671.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _671

        return self.__parent__._cast(_671.BevelGearISOMaterialDatabase)

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
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_678.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _678

        return self.__parent__._cast(_678.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_679.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _679

        return self.__parent__._cast(_679.CylindricalGearPlasticMaterialDatabase)

    @property
    def general_electric_machine_material_database(
        self: "CastSelf",
    ) -> "_1398.GeneralElectricMachineMaterialDatabase":
        from mastapy._private.electric_machines import _1398

        return self.__parent__._cast(_1398.GeneralElectricMachineMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1412.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1412

        return self.__parent__._cast(_1412.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1431.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1431

        return self.__parent__._cast(_1431.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1446.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1446

        return self.__parent__._cast(_1446.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1633.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1633

        return self.__parent__._cast(_1633.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1640.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1640

        return self.__parent__._cast(_1640.RingPinsMaterialDatabase)

    @property
    def material_database(self: "CastSelf") -> "MaterialDatabase":
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
class MaterialDatabase(_2010.NamedDatabase[T]):
    """MaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_MaterialDatabase
        """
        return _Cast_MaterialDatabase(self)
