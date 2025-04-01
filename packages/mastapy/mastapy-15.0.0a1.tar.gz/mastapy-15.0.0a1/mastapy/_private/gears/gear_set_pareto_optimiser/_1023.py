"""ParetoCylindricalRatingOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1726

_PARETO_CYLINDRICAL_RATING_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "ParetoCylindricalRatingOptimisationStrategyDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import _1021, _1022
    from mastapy._private.math_utility.optimisation import _1714
    from mastapy._private.utility.databases import _2006, _2010, _2014

    Self = TypeVar("Self", bound="ParetoCylindricalRatingOptimisationStrategyDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoCylindricalRatingOptimisationStrategyDatabase._Cast_ParetoCylindricalRatingOptimisationStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoCylindricalRatingOptimisationStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoCylindricalRatingOptimisationStrategyDatabase:
    """Special nested class for casting ParetoCylindricalRatingOptimisationStrategyDatabase to subclasses."""

    __parent__: "ParetoCylindricalRatingOptimisationStrategyDatabase"

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1726.ParetoOptimisationStrategyDatabase":
        return self.__parent__._cast(_1726.ParetoOptimisationStrategyDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1714.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1714

        return self.__parent__._cast(_1714.DesignSpaceSearchStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_2010.NamedDatabase":
        pass

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
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1021.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1021

        return self.__parent__._cast(
            _1021.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1022.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1022

        return self.__parent__._cast(
            _1022.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "ParetoCylindricalRatingOptimisationStrategyDatabase":
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
class ParetoCylindricalRatingOptimisationStrategyDatabase(
    _1726.ParetoOptimisationStrategyDatabase
):
    """ParetoCylindricalRatingOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_CYLINDRICAL_RATING_OPTIMISATION_STRATEGY_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ParetoCylindricalRatingOptimisationStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_ParetoCylindricalRatingOptimisationStrategyDatabase
        """
        return _Cast_ParetoCylindricalRatingOptimisationStrategyDatabase(self)
