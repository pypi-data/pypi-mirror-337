"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1641 import AxialLoadType
    from mastapy._private.bolts._1642 import BoltedJointMaterial
    from mastapy._private.bolts._1643 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1644 import BoltGeometry
    from mastapy._private.bolts._1645 import BoltGeometryDatabase
    from mastapy._private.bolts._1646 import BoltMaterial
    from mastapy._private.bolts._1647 import BoltMaterialDatabase
    from mastapy._private.bolts._1648 import BoltSection
    from mastapy._private.bolts._1649 import BoltShankType
    from mastapy._private.bolts._1650 import BoltTypes
    from mastapy._private.bolts._1651 import ClampedSection
    from mastapy._private.bolts._1652 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1653 import DetailedBoltDesign
    from mastapy._private.bolts._1654 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1655 import HeadCapTypes
    from mastapy._private.bolts._1656 import JointGeometries
    from mastapy._private.bolts._1657 import JointTypes
    from mastapy._private.bolts._1658 import LoadedBolt
    from mastapy._private.bolts._1659 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1660 import StandardSizes
    from mastapy._private.bolts._1661 import StrengthGrades
    from mastapy._private.bolts._1662 import ThreadTypes
    from mastapy._private.bolts._1663 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1641": ["AxialLoadType"],
        "_private.bolts._1642": ["BoltedJointMaterial"],
        "_private.bolts._1643": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1644": ["BoltGeometry"],
        "_private.bolts._1645": ["BoltGeometryDatabase"],
        "_private.bolts._1646": ["BoltMaterial"],
        "_private.bolts._1647": ["BoltMaterialDatabase"],
        "_private.bolts._1648": ["BoltSection"],
        "_private.bolts._1649": ["BoltShankType"],
        "_private.bolts._1650": ["BoltTypes"],
        "_private.bolts._1651": ["ClampedSection"],
        "_private.bolts._1652": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1653": ["DetailedBoltDesign"],
        "_private.bolts._1654": ["DetailedBoltedJointDesign"],
        "_private.bolts._1655": ["HeadCapTypes"],
        "_private.bolts._1656": ["JointGeometries"],
        "_private.bolts._1657": ["JointTypes"],
        "_private.bolts._1658": ["LoadedBolt"],
        "_private.bolts._1659": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1660": ["StandardSizes"],
        "_private.bolts._1661": ["StrengthGrades"],
        "_private.bolts._1662": ["ThreadTypes"],
        "_private.bolts._1663": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
