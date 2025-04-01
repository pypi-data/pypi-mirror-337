"""NodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _151

_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "NodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _130,
        _131,
        _136,
        _137,
        _140,
        _141,
        _142,
        _144,
        _147,
        _148,
        _153,
        _154,
        _155,
        _156,
        _159,
        _160,
        _161,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force import (
        _165,
        _166,
        _167,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3011,
    )

    Self = TypeVar("Self", bound="NodalComponent")
    CastSelf = TypeVar("CastSelf", bound="NodalComponent._Cast_NodalComponent")


__docformat__ = "restructuredtext en"
__all__ = ("NodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalComponent:
    """Special nested class for casting NodalComponent to subclasses."""

    __parent__: "NodalComponent"

    @property
    def nodal_entity(self: "CastSelf") -> "_151.NodalEntity":
        return self.__parent__._cast(_151.NodalEntity)

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_130.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.ArbitraryNodalComponent)

    @property
    def bar(self: "CastSelf") -> "_131.Bar":
        from mastapy._private.nodal_analysis.nodal_entities import _131

        return self.__parent__._cast(_131.Bar)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_136.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _136

        return self.__parent__._cast(_136.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_137.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _137

        return self.__parent__._cast(_137.CMSNodalComponent)

    @property
    def distributed_rigid_bar_coupling(
        self: "CastSelf",
    ) -> "_140.DistributedRigidBarCoupling":
        from mastapy._private.nodal_analysis.nodal_entities import _140

        return self.__parent__._cast(_140.DistributedRigidBarCoupling)

    @property
    def flow_junction_nodal_component(
        self: "CastSelf",
    ) -> "_141.FlowJunctionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.FlowJunctionNodalComponent)

    @property
    def friction_nodal_component(self: "CastSelf") -> "_142.FrictionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.FrictionNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_144.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _144

        return self.__parent__._cast(_144.GearMeshNodePair)

    @property
    def inertial_force_component(self: "CastSelf") -> "_147.InertialForceComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _147

        return self.__parent__._cast(_147.InertialForceComponent)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_148.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.LineContactStiffnessEntity)

    @property
    def pid_control_nodal_component(
        self: "CastSelf",
    ) -> "_153.PIDControlNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _153

        return self.__parent__._cast(_153.PIDControlNodalComponent)

    @property
    def pressure_and_volumetric_flow_rate_nodal_component_v2(
        self: "CastSelf",
    ) -> "_154.PressureAndVolumetricFlowRateNodalComponentV2":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(_154.PressureAndVolumetricFlowRateNodalComponentV2)

    @property
    def pressure_constraint_nodal_component(
        self: "CastSelf",
    ) -> "_155.PressureConstraintNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.PressureConstraintNodalComponent)

    @property
    def rigid_bar(self: "CastSelf") -> "_156.RigidBar":
        from mastapy._private.nodal_analysis.nodal_entities import _156

        return self.__parent__._cast(_156.RigidBar)

    @property
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_159.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _159

        return self.__parent__._cast(_159.SurfaceToSurfaceContactStiffnessEntity)

    @property
    def thermal_connector_with_resistance_nodal_component(
        self: "CastSelf",
    ) -> "_160.ThermalConnectorWithResistanceNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _160

        return self.__parent__._cast(_160.ThermalConnectorWithResistanceNodalComponent)

    @property
    def thermal_nodal_component(self: "CastSelf") -> "_161.ThermalNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _161

        return self.__parent__._cast(_161.ThermalNodalComponent)

    @property
    def external_force_entity(self: "CastSelf") -> "_165.ExternalForceEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _165

        return self.__parent__._cast(_165.ExternalForceEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "_166.ExternalForceLineContactEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _166

        return self.__parent__._cast(_166.ExternalForceLineContactEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "_167.ExternalForceSinglePointEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _167

        return self.__parent__._cast(_167.ExternalForceSinglePointEntity)

    @property
    def shaft_section_system_deflection(
        self: "CastSelf",
    ) -> "_3011.ShaftSectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3011,
        )

        return self.__parent__._cast(_3011.ShaftSectionSystemDeflection)

    @property
    def nodal_component(self: "CastSelf") -> "NodalComponent":
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
class NodalComponent(_151.NodalEntity):
    """NodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodalComponent":
        """Cast to another type.

        Returns:
            _Cast_NodalComponent
        """
        return _Cast_NodalComponent(self)
