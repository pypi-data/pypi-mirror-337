"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2613 import FELink
    from mastapy._private.system_model.fe.links._2614 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2615 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2616 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2617 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2618 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2619 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2620 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2621 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2622 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2623 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2624 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2625 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2626 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2627 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2613": ["FELink"],
        "_private.system_model.fe.links._2614": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2615": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2616": ["GearMeshFELink"],
        "_private.system_model.fe.links._2617": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2618": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2619": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2620": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2621": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2622": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2623": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2624": ["PointLoadFELink"],
        "_private.system_model.fe.links._2625": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2626": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2627": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
