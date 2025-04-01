"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2533 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2534 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2535 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2536 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2537 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2538 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2539 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2540 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2541 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2542 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2543 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2544 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2545 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2533": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2534": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2535": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2536": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2537": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2538": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2539": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2540": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2541": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2542": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2543": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2544": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2545": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
