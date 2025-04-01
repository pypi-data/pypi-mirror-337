"""MeasurementBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.units_and_measurements import _1785

_MEASUREMENT_BASE = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements", "MeasurementBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.utility import _1772
    from mastapy._private.utility.units_and_measurements.measurements import (
        _1787,
        _1788,
        _1789,
        _1790,
        _1791,
        _1792,
        _1793,
        _1794,
        _1795,
        _1796,
        _1797,
        _1798,
        _1799,
        _1800,
        _1801,
        _1802,
        _1803,
        _1804,
        _1805,
        _1806,
        _1807,
        _1808,
        _1809,
        _1810,
        _1811,
        _1812,
        _1813,
        _1814,
        _1815,
        _1816,
        _1817,
        _1818,
        _1819,
        _1820,
        _1821,
        _1822,
        _1823,
        _1824,
        _1825,
        _1826,
        _1827,
        _1828,
        _1829,
        _1830,
        _1831,
        _1832,
        _1833,
        _1834,
        _1835,
        _1836,
        _1837,
        _1838,
        _1839,
        _1840,
        _1841,
        _1842,
        _1843,
        _1844,
        _1845,
        _1846,
        _1847,
        _1848,
        _1849,
        _1850,
        _1851,
        _1852,
        _1853,
        _1854,
        _1855,
        _1856,
        _1857,
        _1858,
        _1859,
        _1860,
        _1861,
        _1862,
        _1863,
        _1864,
        _1865,
        _1866,
        _1867,
        _1868,
        _1869,
        _1870,
        _1871,
        _1872,
        _1873,
        _1874,
        _1875,
        _1876,
        _1877,
        _1878,
        _1879,
        _1880,
        _1881,
        _1882,
        _1883,
        _1884,
        _1885,
        _1886,
        _1887,
        _1888,
        _1889,
        _1890,
        _1891,
        _1892,
        _1893,
        _1894,
        _1895,
        _1896,
        _1897,
        _1898,
        _1899,
        _1900,
        _1901,
        _1902,
        _1903,
        _1904,
        _1905,
        _1906,
        _1907,
        _1908,
        _1909,
        _1910,
        _1911,
        _1912,
        _1913,
        _1914,
        _1915,
        _1916,
    )

    Self = TypeVar("Self", bound="MeasurementBase")
    CastSelf = TypeVar("CastSelf", bound="MeasurementBase._Cast_MeasurementBase")


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeasurementBase:
    """Special nested class for casting MeasurementBase to subclasses."""

    __parent__: "MeasurementBase"

    @property
    def acceleration(self: "CastSelf") -> "_1787.Acceleration":
        from mastapy._private.utility.units_and_measurements.measurements import _1787

        return self.__parent__._cast(_1787.Acceleration)

    @property
    def angle(self: "CastSelf") -> "_1788.Angle":
        from mastapy._private.utility.units_and_measurements.measurements import _1788

        return self.__parent__._cast(_1788.Angle)

    @property
    def angle_per_unit_temperature(self: "CastSelf") -> "_1789.AnglePerUnitTemperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1789

        return self.__parent__._cast(_1789.AnglePerUnitTemperature)

    @property
    def angle_small(self: "CastSelf") -> "_1790.AngleSmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1790

        return self.__parent__._cast(_1790.AngleSmall)

    @property
    def angle_very_small(self: "CastSelf") -> "_1791.AngleVerySmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1791

        return self.__parent__._cast(_1791.AngleVerySmall)

    @property
    def angular_acceleration(self: "CastSelf") -> "_1792.AngularAcceleration":
        from mastapy._private.utility.units_and_measurements.measurements import _1792

        return self.__parent__._cast(_1792.AngularAcceleration)

    @property
    def angular_compliance(self: "CastSelf") -> "_1793.AngularCompliance":
        from mastapy._private.utility.units_and_measurements.measurements import _1793

        return self.__parent__._cast(_1793.AngularCompliance)

    @property
    def angular_jerk(self: "CastSelf") -> "_1794.AngularJerk":
        from mastapy._private.utility.units_and_measurements.measurements import _1794

        return self.__parent__._cast(_1794.AngularJerk)

    @property
    def angular_stiffness(self: "CastSelf") -> "_1795.AngularStiffness":
        from mastapy._private.utility.units_and_measurements.measurements import _1795

        return self.__parent__._cast(_1795.AngularStiffness)

    @property
    def angular_velocity(self: "CastSelf") -> "_1796.AngularVelocity":
        from mastapy._private.utility.units_and_measurements.measurements import _1796

        return self.__parent__._cast(_1796.AngularVelocity)

    @property
    def area(self: "CastSelf") -> "_1797.Area":
        from mastapy._private.utility.units_and_measurements.measurements import _1797

        return self.__parent__._cast(_1797.Area)

    @property
    def area_small(self: "CastSelf") -> "_1798.AreaSmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1798

        return self.__parent__._cast(_1798.AreaSmall)

    @property
    def carbon_emission_factor(self: "CastSelf") -> "_1799.CarbonEmissionFactor":
        from mastapy._private.utility.units_and_measurements.measurements import _1799

        return self.__parent__._cast(_1799.CarbonEmissionFactor)

    @property
    def current_density(self: "CastSelf") -> "_1800.CurrentDensity":
        from mastapy._private.utility.units_and_measurements.measurements import _1800

        return self.__parent__._cast(_1800.CurrentDensity)

    @property
    def current_per_length(self: "CastSelf") -> "_1801.CurrentPerLength":
        from mastapy._private.utility.units_and_measurements.measurements import _1801

        return self.__parent__._cast(_1801.CurrentPerLength)

    @property
    def cycles(self: "CastSelf") -> "_1802.Cycles":
        from mastapy._private.utility.units_and_measurements.measurements import _1802

        return self.__parent__._cast(_1802.Cycles)

    @property
    def damage(self: "CastSelf") -> "_1803.Damage":
        from mastapy._private.utility.units_and_measurements.measurements import _1803

        return self.__parent__._cast(_1803.Damage)

    @property
    def damage_rate(self: "CastSelf") -> "_1804.DamageRate":
        from mastapy._private.utility.units_and_measurements.measurements import _1804

        return self.__parent__._cast(_1804.DamageRate)

    @property
    def data_size(self: "CastSelf") -> "_1805.DataSize":
        from mastapy._private.utility.units_and_measurements.measurements import _1805

        return self.__parent__._cast(_1805.DataSize)

    @property
    def decibel(self: "CastSelf") -> "_1806.Decibel":
        from mastapy._private.utility.units_and_measurements.measurements import _1806

        return self.__parent__._cast(_1806.Decibel)

    @property
    def density(self: "CastSelf") -> "_1807.Density":
        from mastapy._private.utility.units_and_measurements.measurements import _1807

        return self.__parent__._cast(_1807.Density)

    @property
    def electrical_resistance(self: "CastSelf") -> "_1808.ElectricalResistance":
        from mastapy._private.utility.units_and_measurements.measurements import _1808

        return self.__parent__._cast(_1808.ElectricalResistance)

    @property
    def electrical_resistivity(self: "CastSelf") -> "_1809.ElectricalResistivity":
        from mastapy._private.utility.units_and_measurements.measurements import _1809

        return self.__parent__._cast(_1809.ElectricalResistivity)

    @property
    def electric_current(self: "CastSelf") -> "_1810.ElectricCurrent":
        from mastapy._private.utility.units_and_measurements.measurements import _1810

        return self.__parent__._cast(_1810.ElectricCurrent)

    @property
    def energy(self: "CastSelf") -> "_1811.Energy":
        from mastapy._private.utility.units_and_measurements.measurements import _1811

        return self.__parent__._cast(_1811.Energy)

    @property
    def energy_per_unit_area(self: "CastSelf") -> "_1812.EnergyPerUnitArea":
        from mastapy._private.utility.units_and_measurements.measurements import _1812

        return self.__parent__._cast(_1812.EnergyPerUnitArea)

    @property
    def energy_per_unit_area_small(self: "CastSelf") -> "_1813.EnergyPerUnitAreaSmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1813

        return self.__parent__._cast(_1813.EnergyPerUnitAreaSmall)

    @property
    def energy_small(self: "CastSelf") -> "_1814.EnergySmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1814

        return self.__parent__._cast(_1814.EnergySmall)

    @property
    def enum(self: "CastSelf") -> "_1815.Enum":
        from mastapy._private.utility.units_and_measurements.measurements import _1815

        return self.__parent__._cast(_1815.Enum)

    @property
    def flow_rate(self: "CastSelf") -> "_1816.FlowRate":
        from mastapy._private.utility.units_and_measurements.measurements import _1816

        return self.__parent__._cast(_1816.FlowRate)

    @property
    def flow_resistance(self: "CastSelf") -> "_1817.FlowResistance":
        from mastapy._private.utility.units_and_measurements.measurements import _1817

        return self.__parent__._cast(_1817.FlowResistance)

    @property
    def force(self: "CastSelf") -> "_1818.Force":
        from mastapy._private.utility.units_and_measurements.measurements import _1818

        return self.__parent__._cast(_1818.Force)

    @property
    def force_per_unit_length(self: "CastSelf") -> "_1819.ForcePerUnitLength":
        from mastapy._private.utility.units_and_measurements.measurements import _1819

        return self.__parent__._cast(_1819.ForcePerUnitLength)

    @property
    def force_per_unit_pressure(self: "CastSelf") -> "_1820.ForcePerUnitPressure":
        from mastapy._private.utility.units_and_measurements.measurements import _1820

        return self.__parent__._cast(_1820.ForcePerUnitPressure)

    @property
    def force_per_unit_temperature(self: "CastSelf") -> "_1821.ForcePerUnitTemperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1821

        return self.__parent__._cast(_1821.ForcePerUnitTemperature)

    @property
    def fraction_measurement_base(self: "CastSelf") -> "_1822.FractionMeasurementBase":
        from mastapy._private.utility.units_and_measurements.measurements import _1822

        return self.__parent__._cast(_1822.FractionMeasurementBase)

    @property
    def fraction_per_temperature(self: "CastSelf") -> "_1823.FractionPerTemperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1823

        return self.__parent__._cast(_1823.FractionPerTemperature)

    @property
    def frequency(self: "CastSelf") -> "_1824.Frequency":
        from mastapy._private.utility.units_and_measurements.measurements import _1824

        return self.__parent__._cast(_1824.Frequency)

    @property
    def fuel_consumption_engine(self: "CastSelf") -> "_1825.FuelConsumptionEngine":
        from mastapy._private.utility.units_and_measurements.measurements import _1825

        return self.__parent__._cast(_1825.FuelConsumptionEngine)

    @property
    def fuel_efficiency_vehicle(self: "CastSelf") -> "_1826.FuelEfficiencyVehicle":
        from mastapy._private.utility.units_and_measurements.measurements import _1826

        return self.__parent__._cast(_1826.FuelEfficiencyVehicle)

    @property
    def gradient(self: "CastSelf") -> "_1827.Gradient":
        from mastapy._private.utility.units_and_measurements.measurements import _1827

        return self.__parent__._cast(_1827.Gradient)

    @property
    def heat_conductivity(self: "CastSelf") -> "_1828.HeatConductivity":
        from mastapy._private.utility.units_and_measurements.measurements import _1828

        return self.__parent__._cast(_1828.HeatConductivity)

    @property
    def heat_transfer(self: "CastSelf") -> "_1829.HeatTransfer":
        from mastapy._private.utility.units_and_measurements.measurements import _1829

        return self.__parent__._cast(_1829.HeatTransfer)

    @property
    def heat_transfer_coefficient_for_plastic_gear_tooth(
        self: "CastSelf",
    ) -> "_1830.HeatTransferCoefficientForPlasticGearTooth":
        from mastapy._private.utility.units_and_measurements.measurements import _1830

        return self.__parent__._cast(_1830.HeatTransferCoefficientForPlasticGearTooth)

    @property
    def heat_transfer_resistance(self: "CastSelf") -> "_1831.HeatTransferResistance":
        from mastapy._private.utility.units_and_measurements.measurements import _1831

        return self.__parent__._cast(_1831.HeatTransferResistance)

    @property
    def impulse(self: "CastSelf") -> "_1832.Impulse":
        from mastapy._private.utility.units_and_measurements.measurements import _1832

        return self.__parent__._cast(_1832.Impulse)

    @property
    def index(self: "CastSelf") -> "_1833.Index":
        from mastapy._private.utility.units_and_measurements.measurements import _1833

        return self.__parent__._cast(_1833.Index)

    @property
    def inductance(self: "CastSelf") -> "_1834.Inductance":
        from mastapy._private.utility.units_and_measurements.measurements import _1834

        return self.__parent__._cast(_1834.Inductance)

    @property
    def integer(self: "CastSelf") -> "_1835.Integer":
        from mastapy._private.utility.units_and_measurements.measurements import _1835

        return self.__parent__._cast(_1835.Integer)

    @property
    def inverse_short_length(self: "CastSelf") -> "_1836.InverseShortLength":
        from mastapy._private.utility.units_and_measurements.measurements import _1836

        return self.__parent__._cast(_1836.InverseShortLength)

    @property
    def inverse_short_time(self: "CastSelf") -> "_1837.InverseShortTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1837

        return self.__parent__._cast(_1837.InverseShortTime)

    @property
    def jerk(self: "CastSelf") -> "_1838.Jerk":
        from mastapy._private.utility.units_and_measurements.measurements import _1838

        return self.__parent__._cast(_1838.Jerk)

    @property
    def kinematic_viscosity(self: "CastSelf") -> "_1839.KinematicViscosity":
        from mastapy._private.utility.units_and_measurements.measurements import _1839

        return self.__parent__._cast(_1839.KinematicViscosity)

    @property
    def length_long(self: "CastSelf") -> "_1840.LengthLong":
        from mastapy._private.utility.units_and_measurements.measurements import _1840

        return self.__parent__._cast(_1840.LengthLong)

    @property
    def length_medium(self: "CastSelf") -> "_1841.LengthMedium":
        from mastapy._private.utility.units_and_measurements.measurements import _1841

        return self.__parent__._cast(_1841.LengthMedium)

    @property
    def length_per_unit_temperature(
        self: "CastSelf",
    ) -> "_1842.LengthPerUnitTemperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1842

        return self.__parent__._cast(_1842.LengthPerUnitTemperature)

    @property
    def length_short(self: "CastSelf") -> "_1843.LengthShort":
        from mastapy._private.utility.units_and_measurements.measurements import _1843

        return self.__parent__._cast(_1843.LengthShort)

    @property
    def length_to_the_fourth(self: "CastSelf") -> "_1844.LengthToTheFourth":
        from mastapy._private.utility.units_and_measurements.measurements import _1844

        return self.__parent__._cast(_1844.LengthToTheFourth)

    @property
    def length_very_long(self: "CastSelf") -> "_1845.LengthVeryLong":
        from mastapy._private.utility.units_and_measurements.measurements import _1845

        return self.__parent__._cast(_1845.LengthVeryLong)

    @property
    def length_very_short(self: "CastSelf") -> "_1846.LengthVeryShort":
        from mastapy._private.utility.units_and_measurements.measurements import _1846

        return self.__parent__._cast(_1846.LengthVeryShort)

    @property
    def length_very_short_per_length_short(
        self: "CastSelf",
    ) -> "_1847.LengthVeryShortPerLengthShort":
        from mastapy._private.utility.units_and_measurements.measurements import _1847

        return self.__parent__._cast(_1847.LengthVeryShortPerLengthShort)

    @property
    def linear_angular_damping(self: "CastSelf") -> "_1848.LinearAngularDamping":
        from mastapy._private.utility.units_and_measurements.measurements import _1848

        return self.__parent__._cast(_1848.LinearAngularDamping)

    @property
    def linear_angular_stiffness_cross_term(
        self: "CastSelf",
    ) -> "_1849.LinearAngularStiffnessCrossTerm":
        from mastapy._private.utility.units_and_measurements.measurements import _1849

        return self.__parent__._cast(_1849.LinearAngularStiffnessCrossTerm)

    @property
    def linear_damping(self: "CastSelf") -> "_1850.LinearDamping":
        from mastapy._private.utility.units_and_measurements.measurements import _1850

        return self.__parent__._cast(_1850.LinearDamping)

    @property
    def linear_flexibility(self: "CastSelf") -> "_1851.LinearFlexibility":
        from mastapy._private.utility.units_and_measurements.measurements import _1851

        return self.__parent__._cast(_1851.LinearFlexibility)

    @property
    def linear_stiffness(self: "CastSelf") -> "_1852.LinearStiffness":
        from mastapy._private.utility.units_and_measurements.measurements import _1852

        return self.__parent__._cast(_1852.LinearStiffness)

    @property
    def magnetic_field_strength(self: "CastSelf") -> "_1853.MagneticFieldStrength":
        from mastapy._private.utility.units_and_measurements.measurements import _1853

        return self.__parent__._cast(_1853.MagneticFieldStrength)

    @property
    def magnetic_flux(self: "CastSelf") -> "_1854.MagneticFlux":
        from mastapy._private.utility.units_and_measurements.measurements import _1854

        return self.__parent__._cast(_1854.MagneticFlux)

    @property
    def magnetic_flux_density(self: "CastSelf") -> "_1855.MagneticFluxDensity":
        from mastapy._private.utility.units_and_measurements.measurements import _1855

        return self.__parent__._cast(_1855.MagneticFluxDensity)

    @property
    def magnetic_vector_potential(self: "CastSelf") -> "_1856.MagneticVectorPotential":
        from mastapy._private.utility.units_and_measurements.measurements import _1856

        return self.__parent__._cast(_1856.MagneticVectorPotential)

    @property
    def magnetomotive_force(self: "CastSelf") -> "_1857.MagnetomotiveForce":
        from mastapy._private.utility.units_and_measurements.measurements import _1857

        return self.__parent__._cast(_1857.MagnetomotiveForce)

    @property
    def mass(self: "CastSelf") -> "_1858.Mass":
        from mastapy._private.utility.units_and_measurements.measurements import _1858

        return self.__parent__._cast(_1858.Mass)

    @property
    def mass_per_unit_length(self: "CastSelf") -> "_1859.MassPerUnitLength":
        from mastapy._private.utility.units_and_measurements.measurements import _1859

        return self.__parent__._cast(_1859.MassPerUnitLength)

    @property
    def mass_per_unit_time(self: "CastSelf") -> "_1860.MassPerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1860

        return self.__parent__._cast(_1860.MassPerUnitTime)

    @property
    def moment_of_inertia(self: "CastSelf") -> "_1861.MomentOfInertia":
        from mastapy._private.utility.units_and_measurements.measurements import _1861

        return self.__parent__._cast(_1861.MomentOfInertia)

    @property
    def moment_of_inertia_per_unit_length(
        self: "CastSelf",
    ) -> "_1862.MomentOfInertiaPerUnitLength":
        from mastapy._private.utility.units_and_measurements.measurements import _1862

        return self.__parent__._cast(_1862.MomentOfInertiaPerUnitLength)

    @property
    def moment_per_unit_pressure(self: "CastSelf") -> "_1863.MomentPerUnitPressure":
        from mastapy._private.utility.units_and_measurements.measurements import _1863

        return self.__parent__._cast(_1863.MomentPerUnitPressure)

    @property
    def number(self: "CastSelf") -> "_1864.Number":
        from mastapy._private.utility.units_and_measurements.measurements import _1864

        return self.__parent__._cast(_1864.Number)

    @property
    def percentage(self: "CastSelf") -> "_1865.Percentage":
        from mastapy._private.utility.units_and_measurements.measurements import _1865

        return self.__parent__._cast(_1865.Percentage)

    @property
    def power(self: "CastSelf") -> "_1866.Power":
        from mastapy._private.utility.units_and_measurements.measurements import _1866

        return self.__parent__._cast(_1866.Power)

    @property
    def power_per_small_area(self: "CastSelf") -> "_1867.PowerPerSmallArea":
        from mastapy._private.utility.units_and_measurements.measurements import _1867

        return self.__parent__._cast(_1867.PowerPerSmallArea)

    @property
    def power_per_unit_time(self: "CastSelf") -> "_1868.PowerPerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1868

        return self.__parent__._cast(_1868.PowerPerUnitTime)

    @property
    def power_small(self: "CastSelf") -> "_1869.PowerSmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1869

        return self.__parent__._cast(_1869.PowerSmall)

    @property
    def power_small_per_area(self: "CastSelf") -> "_1870.PowerSmallPerArea":
        from mastapy._private.utility.units_and_measurements.measurements import _1870

        return self.__parent__._cast(_1870.PowerSmallPerArea)

    @property
    def power_small_per_mass(self: "CastSelf") -> "_1871.PowerSmallPerMass":
        from mastapy._private.utility.units_and_measurements.measurements import _1871

        return self.__parent__._cast(_1871.PowerSmallPerMass)

    @property
    def power_small_per_unit_area_per_unit_time(
        self: "CastSelf",
    ) -> "_1872.PowerSmallPerUnitAreaPerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1872

        return self.__parent__._cast(_1872.PowerSmallPerUnitAreaPerUnitTime)

    @property
    def power_small_per_unit_time(self: "CastSelf") -> "_1873.PowerSmallPerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1873

        return self.__parent__._cast(_1873.PowerSmallPerUnitTime)

    @property
    def power_small_per_volume(self: "CastSelf") -> "_1874.PowerSmallPerVolume":
        from mastapy._private.utility.units_and_measurements.measurements import _1874

        return self.__parent__._cast(_1874.PowerSmallPerVolume)

    @property
    def pressure(self: "CastSelf") -> "_1875.Pressure":
        from mastapy._private.utility.units_and_measurements.measurements import _1875

        return self.__parent__._cast(_1875.Pressure)

    @property
    def pressure_per_unit_time(self: "CastSelf") -> "_1876.PressurePerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1876

        return self.__parent__._cast(_1876.PressurePerUnitTime)

    @property
    def pressure_small(self: "CastSelf") -> "_1877.PressureSmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1877

        return self.__parent__._cast(_1877.PressureSmall)

    @property
    def pressure_velocity_product(self: "CastSelf") -> "_1878.PressureVelocityProduct":
        from mastapy._private.utility.units_and_measurements.measurements import _1878

        return self.__parent__._cast(_1878.PressureVelocityProduct)

    @property
    def pressure_viscosity_coefficient(
        self: "CastSelf",
    ) -> "_1879.PressureViscosityCoefficient":
        from mastapy._private.utility.units_and_measurements.measurements import _1879

        return self.__parent__._cast(_1879.PressureViscosityCoefficient)

    @property
    def price(self: "CastSelf") -> "_1880.Price":
        from mastapy._private.utility.units_and_measurements.measurements import _1880

        return self.__parent__._cast(_1880.Price)

    @property
    def price_per_unit_mass(self: "CastSelf") -> "_1881.PricePerUnitMass":
        from mastapy._private.utility.units_and_measurements.measurements import _1881

        return self.__parent__._cast(_1881.PricePerUnitMass)

    @property
    def quadratic_angular_damping(self: "CastSelf") -> "_1882.QuadraticAngularDamping":
        from mastapy._private.utility.units_and_measurements.measurements import _1882

        return self.__parent__._cast(_1882.QuadraticAngularDamping)

    @property
    def quadratic_drag(self: "CastSelf") -> "_1883.QuadraticDrag":
        from mastapy._private.utility.units_and_measurements.measurements import _1883

        return self.__parent__._cast(_1883.QuadraticDrag)

    @property
    def rescaled_measurement(self: "CastSelf") -> "_1884.RescaledMeasurement":
        from mastapy._private.utility.units_and_measurements.measurements import _1884

        return self.__parent__._cast(_1884.RescaledMeasurement)

    @property
    def rotatum(self: "CastSelf") -> "_1885.Rotatum":
        from mastapy._private.utility.units_and_measurements.measurements import _1885

        return self.__parent__._cast(_1885.Rotatum)

    @property
    def safety_factor(self: "CastSelf") -> "_1886.SafetyFactor":
        from mastapy._private.utility.units_and_measurements.measurements import _1886

        return self.__parent__._cast(_1886.SafetyFactor)

    @property
    def specific_acoustic_impedance(
        self: "CastSelf",
    ) -> "_1887.SpecificAcousticImpedance":
        from mastapy._private.utility.units_and_measurements.measurements import _1887

        return self.__parent__._cast(_1887.SpecificAcousticImpedance)

    @property
    def specific_heat(self: "CastSelf") -> "_1888.SpecificHeat":
        from mastapy._private.utility.units_and_measurements.measurements import _1888

        return self.__parent__._cast(_1888.SpecificHeat)

    @property
    def square_root_of_unit_force_per_unit_area(
        self: "CastSelf",
    ) -> "_1889.SquareRootOfUnitForcePerUnitArea":
        from mastapy._private.utility.units_and_measurements.measurements import _1889

        return self.__parent__._cast(_1889.SquareRootOfUnitForcePerUnitArea)

    @property
    def stiffness_per_unit_face_width(
        self: "CastSelf",
    ) -> "_1890.StiffnessPerUnitFaceWidth":
        from mastapy._private.utility.units_and_measurements.measurements import _1890

        return self.__parent__._cast(_1890.StiffnessPerUnitFaceWidth)

    @property
    def stress(self: "CastSelf") -> "_1891.Stress":
        from mastapy._private.utility.units_and_measurements.measurements import _1891

        return self.__parent__._cast(_1891.Stress)

    @property
    def temperature(self: "CastSelf") -> "_1892.Temperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1892

        return self.__parent__._cast(_1892.Temperature)

    @property
    def temperature_difference(self: "CastSelf") -> "_1893.TemperatureDifference":
        from mastapy._private.utility.units_and_measurements.measurements import _1893

        return self.__parent__._cast(_1893.TemperatureDifference)

    @property
    def temperature_per_unit_time(self: "CastSelf") -> "_1894.TemperaturePerUnitTime":
        from mastapy._private.utility.units_and_measurements.measurements import _1894

        return self.__parent__._cast(_1894.TemperaturePerUnitTime)

    @property
    def text(self: "CastSelf") -> "_1895.Text":
        from mastapy._private.utility.units_and_measurements.measurements import _1895

        return self.__parent__._cast(_1895.Text)

    @property
    def thermal_contact_coefficient(
        self: "CastSelf",
    ) -> "_1896.ThermalContactCoefficient":
        from mastapy._private.utility.units_and_measurements.measurements import _1896

        return self.__parent__._cast(_1896.ThermalContactCoefficient)

    @property
    def thermal_expansion_coefficient(
        self: "CastSelf",
    ) -> "_1897.ThermalExpansionCoefficient":
        from mastapy._private.utility.units_and_measurements.measurements import _1897

        return self.__parent__._cast(_1897.ThermalExpansionCoefficient)

    @property
    def thermal_resistance(self: "CastSelf") -> "_1898.ThermalResistance":
        from mastapy._private.utility.units_and_measurements.measurements import _1898

        return self.__parent__._cast(_1898.ThermalResistance)

    @property
    def thermo_elastic_factor(self: "CastSelf") -> "_1899.ThermoElasticFactor":
        from mastapy._private.utility.units_and_measurements.measurements import _1899

        return self.__parent__._cast(_1899.ThermoElasticFactor)

    @property
    def time(self: "CastSelf") -> "_1900.Time":
        from mastapy._private.utility.units_and_measurements.measurements import _1900

        return self.__parent__._cast(_1900.Time)

    @property
    def time_short(self: "CastSelf") -> "_1901.TimeShort":
        from mastapy._private.utility.units_and_measurements.measurements import _1901

        return self.__parent__._cast(_1901.TimeShort)

    @property
    def time_very_short(self: "CastSelf") -> "_1902.TimeVeryShort":
        from mastapy._private.utility.units_and_measurements.measurements import _1902

        return self.__parent__._cast(_1902.TimeVeryShort)

    @property
    def torque(self: "CastSelf") -> "_1903.Torque":
        from mastapy._private.utility.units_and_measurements.measurements import _1903

        return self.__parent__._cast(_1903.Torque)

    @property
    def torque_converter_inverse_k(self: "CastSelf") -> "_1904.TorqueConverterInverseK":
        from mastapy._private.utility.units_and_measurements.measurements import _1904

        return self.__parent__._cast(_1904.TorqueConverterInverseK)

    @property
    def torque_converter_k(self: "CastSelf") -> "_1905.TorqueConverterK":
        from mastapy._private.utility.units_and_measurements.measurements import _1905

        return self.__parent__._cast(_1905.TorqueConverterK)

    @property
    def torque_per_current(self: "CastSelf") -> "_1906.TorquePerCurrent":
        from mastapy._private.utility.units_and_measurements.measurements import _1906

        return self.__parent__._cast(_1906.TorquePerCurrent)

    @property
    def torque_per_square_root_of_power(
        self: "CastSelf",
    ) -> "_1907.TorquePerSquareRootOfPower":
        from mastapy._private.utility.units_and_measurements.measurements import _1907

        return self.__parent__._cast(_1907.TorquePerSquareRootOfPower)

    @property
    def torque_per_unit_temperature(
        self: "CastSelf",
    ) -> "_1908.TorquePerUnitTemperature":
        from mastapy._private.utility.units_and_measurements.measurements import _1908

        return self.__parent__._cast(_1908.TorquePerUnitTemperature)

    @property
    def velocity(self: "CastSelf") -> "_1909.Velocity":
        from mastapy._private.utility.units_and_measurements.measurements import _1909

        return self.__parent__._cast(_1909.Velocity)

    @property
    def velocity_small(self: "CastSelf") -> "_1910.VelocitySmall":
        from mastapy._private.utility.units_and_measurements.measurements import _1910

        return self.__parent__._cast(_1910.VelocitySmall)

    @property
    def viscosity(self: "CastSelf") -> "_1911.Viscosity":
        from mastapy._private.utility.units_and_measurements.measurements import _1911

        return self.__parent__._cast(_1911.Viscosity)

    @property
    def voltage(self: "CastSelf") -> "_1912.Voltage":
        from mastapy._private.utility.units_and_measurements.measurements import _1912

        return self.__parent__._cast(_1912.Voltage)

    @property
    def voltage_per_angular_velocity(
        self: "CastSelf",
    ) -> "_1913.VoltagePerAngularVelocity":
        from mastapy._private.utility.units_and_measurements.measurements import _1913

        return self.__parent__._cast(_1913.VoltagePerAngularVelocity)

    @property
    def volume(self: "CastSelf") -> "_1914.Volume":
        from mastapy._private.utility.units_and_measurements.measurements import _1914

        return self.__parent__._cast(_1914.Volume)

    @property
    def wear_coefficient(self: "CastSelf") -> "_1915.WearCoefficient":
        from mastapy._private.utility.units_and_measurements.measurements import _1915

        return self.__parent__._cast(_1915.WearCoefficient)

    @property
    def yank(self: "CastSelf") -> "_1916.Yank":
        from mastapy._private.utility.units_and_measurements.measurements import _1916

        return self.__parent__._cast(_1916.Yank)

    @property
    def measurement_base(self: "CastSelf") -> "MeasurementBase":
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
class MeasurementBase(_0.APIBase):
    """MeasurementBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASUREMENT_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def absolute_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AbsoluteTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @absolute_tolerance.setter
    @enforce_parameter_types
    def absolute_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AbsoluteTolerance", value)

    @property
    def default_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @default_unit.setter
    @enforce_parameter_types
    def default_unit(self: "Self", value: "_1785.Unit") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "DefaultUnit", value)

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
    def percentage_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PercentageTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @percentage_tolerance.setter
    @enforce_parameter_types
    def percentage_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PercentageTolerance", value)

    @property
    def rounding_digits(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RoundingDigits")

        if temp is None:
            return 0

        return temp

    @rounding_digits.setter
    @enforce_parameter_types
    def rounding_digits(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "RoundingDigits", int(value) if value is not None else 0
        )

    @property
    def rounding_method(self: "Self") -> "_1772.RoundingMethods":
        """mastapy.utility.RoundingMethods"""
        temp = pythonnet_property_get(self.wrapped, "RoundingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Utility.RoundingMethods")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility._1772", "RoundingMethods"
        )(value)

    @rounding_method.setter
    @enforce_parameter_types
    def rounding_method(self: "Self", value: "_1772.RoundingMethods") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Utility.RoundingMethods")
        pythonnet_property_set(self.wrapped, "RoundingMethod", value)

    @property
    def current_unit(self: "Self") -> "_1785.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentUnit")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def available_units(self: "Self") -> "List[_1785.Unit]":
        """List[mastapy.utility.units_and_measurements.Unit]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AvailableUnits")

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
    def cast_to(self: "Self") -> "_Cast_MeasurementBase":
        """Cast to another type.

        Returns:
            _Cast_MeasurementBase
        """
        return _Cast_MeasurementBase(self)
