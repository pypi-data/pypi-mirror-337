"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2693 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2694 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2695 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2696 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2697 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2698 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2699 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2700 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2701 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2702 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2703 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2704 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2705 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2706 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2707 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2708 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2709 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2710 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2711 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2693": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2694": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2695": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2696": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2697": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2698": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2699": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2700": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2701": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2702": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2703": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2704": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2705": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2706": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2707": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2708": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2709": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2710": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2711": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)
