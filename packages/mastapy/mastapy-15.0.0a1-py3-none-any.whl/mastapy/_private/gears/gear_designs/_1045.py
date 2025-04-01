"""GearDesignComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_DESIGN_COMPONENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearDesignComponent"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1044, _1046, _1047
    from mastapy._private.gears.gear_designs.agma_gleason_conical import (
        _1306,
        _1307,
        _1308,
        _1309,
    )
    from mastapy._private.gears.gear_designs.bevel import _1293, _1294, _1295, _1296
    from mastapy._private.gears.gear_designs.concept import _1289, _1290, _1291
    from mastapy._private.gears.gear_designs.conical import _1267, _1268, _1269, _1272
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1115,
        _1121,
        _1131,
        _1144,
        _1145,
    )
    from mastapy._private.gears.gear_designs.face import (
        _1086,
        _1088,
        _1091,
        _1092,
        _1094,
    )
    from mastapy._private.gears.gear_designs.hypoid import _1082, _1083, _1084, _1085
    from mastapy._private.gears.gear_designs.klingelnberg_conical import (
        _1078,
        _1079,
        _1080,
        _1081,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import (
        _1074,
        _1075,
        _1076,
        _1077,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import (
        _1070,
        _1071,
        _1072,
        _1073,
    )
    from mastapy._private.gears.gear_designs.spiral_bevel import (
        _1066,
        _1067,
        _1068,
        _1069,
    )
    from mastapy._private.gears.gear_designs.straight_bevel import (
        _1058,
        _1059,
        _1060,
        _1061,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff import (
        _1062,
        _1063,
        _1064,
        _1065,
    )
    from mastapy._private.gears.gear_designs.worm import (
        _1053,
        _1054,
        _1055,
        _1056,
        _1057,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel import (
        _1049,
        _1050,
        _1051,
        _1052,
    )
    from mastapy._private.utility.scripting import _1919

    Self = TypeVar("Self", bound="GearDesignComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="GearDesignComponent._Cast_GearDesignComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignComponent:
    """Special nested class for casting GearDesignComponent to subclasses."""

    __parent__: "GearDesignComponent"

    @property
    def gear_design(self: "CastSelf") -> "_1044.GearDesign":
        from mastapy._private.gears.gear_designs import _1044

        return self.__parent__._cast(_1044.GearDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_1046.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _1046

        return self.__parent__._cast(_1046.GearMeshDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1047.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1047

        return self.__parent__._cast(_1047.GearSetDesign)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_1049.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1049

        return self.__parent__._cast(_1049.ZerolBevelGearDesign)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1050.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1050

        return self.__parent__._cast(_1050.ZerolBevelGearMeshDesign)

    @property
    def zerol_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1051.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1051

        return self.__parent__._cast(_1051.ZerolBevelGearSetDesign)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1052.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1052

        return self.__parent__._cast(_1052.ZerolBevelMeshedGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_1053.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _1053

        return self.__parent__._cast(_1053.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_1054.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _1054

        return self.__parent__._cast(_1054.WormGearDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_1055.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _1055

        return self.__parent__._cast(_1055.WormGearMeshDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_1056.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _1056

        return self.__parent__._cast(_1056.WormGearSetDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_1057.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _1057

        return self.__parent__._cast(_1057.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_1058.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1058

        return self.__parent__._cast(_1058.StraightBevelGearDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1059.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1059

        return self.__parent__._cast(_1059.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1060.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1060

        return self.__parent__._cast(_1060.StraightBevelGearSetDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1061.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1061

        return self.__parent__._cast(_1061.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_1062.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1062

        return self.__parent__._cast(_1062.StraightBevelDiffGearDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1063.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1063

        return self.__parent__._cast(_1063.StraightBevelDiffGearMeshDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_1064.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1064

        return self.__parent__._cast(_1064.StraightBevelDiffGearSetDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1065.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1065

        return self.__parent__._cast(_1065.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_1066.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1066

        return self.__parent__._cast(_1066.SpiralBevelGearDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1067.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1067

        return self.__parent__._cast(_1067.SpiralBevelGearMeshDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1068.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1068

        return self.__parent__._cast(_1068.SpiralBevelGearSetDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1069.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1069

        return self.__parent__._cast(_1069.SpiralBevelMeshedGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_1070.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1070

        return self.__parent__._cast(
            _1070.KlingelnbergCycloPalloidSpiralBevelGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1071.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1071

        return self.__parent__._cast(
            _1071.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1072.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1072

        return self.__parent__._cast(
            _1072.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1073.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1073

        return self.__parent__._cast(
            _1073.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1074.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1074

        return self.__parent__._cast(_1074.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1075.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1075

        return self.__parent__._cast(_1075.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1076.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1076

        return self.__parent__._cast(_1076.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1077.KlingelnbergCycloPalloidHypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1077

        return self.__parent__._cast(
            _1077.KlingelnbergCycloPalloidHypoidMeshedGearDesign
        )

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1078.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1078

        return self.__parent__._cast(_1078.KlingelnbergConicalGearDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1079.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1079

        return self.__parent__._cast(_1079.KlingelnbergConicalGearMeshDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1080.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1080

        return self.__parent__._cast(_1080.KlingelnbergConicalGearSetDesign)

    @property
    def klingelnberg_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1081.KlingelnbergConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1081

        return self.__parent__._cast(_1081.KlingelnbergConicalMeshedGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1082.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1082

        return self.__parent__._cast(_1082.HypoidGearDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1083.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1083

        return self.__parent__._cast(_1083.HypoidGearMeshDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1084.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1084

        return self.__parent__._cast(_1084.HypoidGearSetDesign)

    @property
    def hypoid_meshed_gear_design(self: "CastSelf") -> "_1085.HypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1085

        return self.__parent__._cast(_1085.HypoidMeshedGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1086.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1086

        return self.__parent__._cast(_1086.FaceGearDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1088.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1088

        return self.__parent__._cast(_1088.FaceGearMeshDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1091.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1091

        return self.__parent__._cast(_1091.FaceGearPinionDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1092.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1092

        return self.__parent__._cast(_1092.FaceGearSetDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1094.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1094

        return self.__parent__._cast(_1094.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1115.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1115

        return self.__parent__._cast(_1115.CylindricalGearDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1121.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1121

        return self.__parent__._cast(_1121.CylindricalGearMeshDesign)

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1131.CylindricalGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1131

        return self.__parent__._cast(_1131.CylindricalGearSetDesign)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1144.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1144

        return self.__parent__._cast(_1144.CylindricalPlanetaryGearSetDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1145.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1145

        return self.__parent__._cast(_1145.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1267.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1267

        return self.__parent__._cast(_1267.ConicalGearDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1268.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1268

        return self.__parent__._cast(_1268.ConicalGearMeshDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1269.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1269

        return self.__parent__._cast(_1269.ConicalGearSetDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1272.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1272

        return self.__parent__._cast(_1272.ConicalMeshedGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1289.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1289

        return self.__parent__._cast(_1289.ConceptGearDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1290.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1290

        return self.__parent__._cast(_1290.ConceptGearMeshDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1291.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1291

        return self.__parent__._cast(_1291.ConceptGearSetDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1293.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1293

        return self.__parent__._cast(_1293.BevelGearDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1294.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1294

        return self.__parent__._cast(_1294.BevelGearMeshDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1295.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1295

        return self.__parent__._cast(_1295.BevelGearSetDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1296.BevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1296

        return self.__parent__._cast(_1296.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1306.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1306

        return self.__parent__._cast(_1306.AGMAGleasonConicalGearDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1307.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1307

        return self.__parent__._cast(_1307.AGMAGleasonConicalGearMeshDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1308.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1308

        return self.__parent__._cast(_1308.AGMAGleasonConicalGearSetDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1309.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1309

        return self.__parent__._cast(_1309.AGMAGleasonConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "GearDesignComponent":
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
class GearDesignComponent(_0.APIBase):
    """GearDesignComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_COMPONENT

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
    def user_specified_data(self: "Self") -> "_1919.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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

    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

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

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignComponent":
        """Cast to another type.

        Returns:
            _Cast_GearDesignComponent
        """
        return _Cast_GearDesignComponent(self)
