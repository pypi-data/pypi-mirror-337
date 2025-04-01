"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.cycloidal._1627 import ContactSpecification
    from mastapy._private.cycloidal._1628 import CrowningSpecificationMethod
    from mastapy._private.cycloidal._1629 import CycloidalAssemblyDesign
    from mastapy._private.cycloidal._1630 import CycloidalDiscDesign
    from mastapy._private.cycloidal._1631 import CycloidalDiscDesignExporter
    from mastapy._private.cycloidal._1632 import CycloidalDiscMaterial
    from mastapy._private.cycloidal._1633 import CycloidalDiscMaterialDatabase
    from mastapy._private.cycloidal._1634 import CycloidalDiscModificationsSpecification
    from mastapy._private.cycloidal._1635 import DirectionOfMeasuredModifications
    from mastapy._private.cycloidal._1636 import GeometryToExport
    from mastapy._private.cycloidal._1637 import NamedDiscPhase
    from mastapy._private.cycloidal._1638 import RingPinsDesign
    from mastapy._private.cycloidal._1639 import RingPinsMaterial
    from mastapy._private.cycloidal._1640 import RingPinsMaterialDatabase
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.cycloidal._1627": ["ContactSpecification"],
        "_private.cycloidal._1628": ["CrowningSpecificationMethod"],
        "_private.cycloidal._1629": ["CycloidalAssemblyDesign"],
        "_private.cycloidal._1630": ["CycloidalDiscDesign"],
        "_private.cycloidal._1631": ["CycloidalDiscDesignExporter"],
        "_private.cycloidal._1632": ["CycloidalDiscMaterial"],
        "_private.cycloidal._1633": ["CycloidalDiscMaterialDatabase"],
        "_private.cycloidal._1634": ["CycloidalDiscModificationsSpecification"],
        "_private.cycloidal._1635": ["DirectionOfMeasuredModifications"],
        "_private.cycloidal._1636": ["GeometryToExport"],
        "_private.cycloidal._1637": ["NamedDiscPhase"],
        "_private.cycloidal._1638": ["RingPinsDesign"],
        "_private.cycloidal._1639": ["RingPinsMaterial"],
        "_private.cycloidal._1640": ["RingPinsMaterialDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactSpecification",
    "CrowningSpecificationMethod",
    "CycloidalAssemblyDesign",
    "CycloidalDiscDesign",
    "CycloidalDiscDesignExporter",
    "CycloidalDiscMaterial",
    "CycloidalDiscMaterialDatabase",
    "CycloidalDiscModificationsSpecification",
    "DirectionOfMeasuredModifications",
    "GeometryToExport",
    "NamedDiscPhase",
    "RingPinsDesign",
    "RingPinsMaterial",
    "RingPinsMaterialDatabase",
)
