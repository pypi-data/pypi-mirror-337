"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2456 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2457 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2458 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2459 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2460 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2461 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2462 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2463 import Connection
    from mastapy._private.system_model.connections_and_sockets._2464 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2465 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2466 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2467 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2468 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2469 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2470 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2471 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2472 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2473 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2474 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2475 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2476 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2477 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2478 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2479 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2480 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2481 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2482 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2483 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2484 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2485 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2486 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2487 import Socket
    from mastapy._private.system_model.connections_and_sockets._2488 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2489 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2456": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2457": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2458": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2459": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2460": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2461": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2462": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2463": ["Connection"],
        "_private.system_model.connections_and_sockets._2464": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2465": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2466": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2467": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2468": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2469": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2470": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2471": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2472": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2473": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2474": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2475": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2476": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2477": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2478": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2479": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2480": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2481": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2482": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2483": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2484": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2485": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2486": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2487": ["Socket"],
        "_private.system_model.connections_and_sockets._2488": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2489": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
