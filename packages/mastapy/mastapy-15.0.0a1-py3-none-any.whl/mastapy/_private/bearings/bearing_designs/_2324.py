"""NonLinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2320

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2321
    from mastapy._private.bearings.bearing_designs.concept import _2388, _2389, _2390
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2378,
        _2380,
        _2382,
        _2384,
        _2385,
        _2386,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2325,
        _2326,
        _2327,
        _2328,
        _2329,
        _2330,
        _2332,
        _2338,
        _2339,
        _2340,
        _2344,
        _2349,
        _2350,
        _2351,
        _2352,
        _2355,
        _2357,
        _2360,
        _2361,
        _2362,
        _2363,
        _2364,
        _2365,
    )

    Self = TypeVar("Self", bound="NonLinearBearing")
    CastSelf = TypeVar("CastSelf", bound="NonLinearBearing._Cast_NonLinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearBearing:
    """Special nested class for casting NonLinearBearing to subclasses."""

    __parent__: "NonLinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2320.BearingDesign":
        return self.__parent__._cast(_2320.BearingDesign)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2321.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2321

        return self.__parent__._cast(_2321.DetailedBearing)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2325.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2325

        return self.__parent__._cast(_2325.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2326.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2326

        return self.__parent__._cast(_2326.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2327.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2327

        return self.__parent__._cast(_2327.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2328.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2328

        return self.__parent__._cast(_2328.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2329.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2329

        return self.__parent__._cast(_2329.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2330.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2330

        return self.__parent__._cast(_2330.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2332.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2332

        return self.__parent__._cast(_2332.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2338.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2338

        return self.__parent__._cast(_2338.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2339.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2339

        return self.__parent__._cast(_2339.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2340.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2340

        return self.__parent__._cast(_2340.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2344.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2344

        return self.__parent__._cast(_2344.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2349.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2349

        return self.__parent__._cast(_2349.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2350.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2350

        return self.__parent__._cast(_2350.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2351.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2351

        return self.__parent__._cast(_2351.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2352.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2352

        return self.__parent__._cast(_2352.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2355.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2355

        return self.__parent__._cast(_2355.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2357.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2357

        return self.__parent__._cast(_2357.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2360.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2360

        return self.__parent__._cast(_2360.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2361.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2361

        return self.__parent__._cast(_2361.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2362.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2362

        return self.__parent__._cast(_2362.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2363.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2363

        return self.__parent__._cast(_2363.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2364.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2364

        return self.__parent__._cast(_2364.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2365.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2365

        return self.__parent__._cast(_2365.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2378.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2378

        return self.__parent__._cast(_2378.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2380.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2380

        return self.__parent__._cast(_2380.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2382.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2382

        return self.__parent__._cast(_2382.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2384.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2384

        return self.__parent__._cast(_2384.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2385.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2385

        return self.__parent__._cast(_2385.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2386.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2386

        return self.__parent__._cast(_2386.TiltingPadThrustBearing)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2388.ConceptAxialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2388

        return self.__parent__._cast(_2388.ConceptAxialClearanceBearing)

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2389.ConceptClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2389

        return self.__parent__._cast(_2389.ConceptClearanceBearing)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2390.ConceptRadialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2390

        return self.__parent__._cast(_2390.ConceptRadialClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "NonLinearBearing":
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
class NonLinearBearing(_2320.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NonLinearBearing":
        """Cast to another type.

        Returns:
            _Cast_NonLinearBearing
        """
        return _Cast_NonLinearBearing(self)
