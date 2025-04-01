"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1199 import (
        CylindricalGearBiasModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1200 import (
        CylindricalGearCommonFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1201 import (
        CylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1202 import (
        CylindricalGearLeadModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1203 import (
        CylindricalGearLeadModificationAtProfilePosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1204 import (
        CylindricalGearMeshMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1205 import (
        CylindricalGearMeshMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1206 import (
        CylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1207 import (
        CylindricalGearMicroGeometryBase,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1208 import (
        CylindricalGearMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1209 import (
        CylindricalGearMicroGeometryMap,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1210 import (
        CylindricalGearMicroGeometryPerTooth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1211 import (
        CylindricalGearProfileModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1212 import (
        CylindricalGearProfileModificationAtFaceWidthPosition,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1213 import (
        CylindricalGearSetMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1214 import (
        CylindricalGearSetMicroGeometryDutyCycle,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1215 import (
        CylindricalGearToothMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1216 import (
        CylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1217 import (
        CylindricalGearTriangularEndModificationAtOrientation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1218 import (
        DrawDefiningGearOrBoth,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1219 import (
        GearAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1220 import (
        LeadFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1221 import (
        LeadModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1222 import (
        LeadReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1223 import (
        LeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1224 import (
        LeadSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1225 import (
        LinearCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1226 import (
        MeasuredMapDataTypes,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1227 import (
        MeshAlignment,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1228 import (
        MeshedCylindricalGearFlankMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1229 import (
        MeshedCylindricalGearMicroGeometry,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1230 import (
        MicroGeometryLeadToleranceChartView,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1231 import (
        MicroGeometryViewingOptions,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1232 import (
        ModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1233 import (
        ParabolicCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1234 import (
        ProfileFormReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1235 import (
        ProfileModificationForCustomer102CAD,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1236 import (
        ProfileReliefSpecificationForCustomer102,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1237 import (
        ProfileReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1238 import (
        ProfileSlopeReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1239 import (
        ReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1240 import (
        SingleCylindricalGearTriangularEndModification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1241 import (
        TotalLeadReliefWithDeviation,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1242 import (
        TotalProfileReliefWithDeviation,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.micro_geometry._1199": [
            "CylindricalGearBiasModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1200": [
            "CylindricalGearCommonFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1201": [
            "CylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1202": [
            "CylindricalGearLeadModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1203": [
            "CylindricalGearLeadModificationAtProfilePosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1204": [
            "CylindricalGearMeshMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1205": [
            "CylindricalGearMeshMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1206": [
            "CylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1207": [
            "CylindricalGearMicroGeometryBase"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1208": [
            "CylindricalGearMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1209": [
            "CylindricalGearMicroGeometryMap"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1210": [
            "CylindricalGearMicroGeometryPerTooth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1211": [
            "CylindricalGearProfileModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1212": [
            "CylindricalGearProfileModificationAtFaceWidthPosition"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1213": [
            "CylindricalGearSetMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1214": [
            "CylindricalGearSetMicroGeometryDutyCycle"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1215": [
            "CylindricalGearToothMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1216": [
            "CylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1217": [
            "CylindricalGearTriangularEndModificationAtOrientation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1218": [
            "DrawDefiningGearOrBoth"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1219": [
            "GearAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1220": [
            "LeadFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1221": [
            "LeadModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1222": [
            "LeadReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1223": [
            "LeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1224": [
            "LeadSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1225": [
            "LinearCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1226": [
            "MeasuredMapDataTypes"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1227": [
            "MeshAlignment"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1228": [
            "MeshedCylindricalGearFlankMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1229": [
            "MeshedCylindricalGearMicroGeometry"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1230": [
            "MicroGeometryLeadToleranceChartView"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1231": [
            "MicroGeometryViewingOptions"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1232": [
            "ModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1233": [
            "ParabolicCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1234": [
            "ProfileFormReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1235": [
            "ProfileModificationForCustomer102CAD"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1236": [
            "ProfileReliefSpecificationForCustomer102"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1237": [
            "ProfileReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1238": [
            "ProfileSlopeReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1239": [
            "ReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1240": [
            "SingleCylindricalGearTriangularEndModification"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1241": [
            "TotalLeadReliefWithDeviation"
        ],
        "_private.gears.gear_designs.cylindrical.micro_geometry._1242": [
            "TotalProfileReliefWithDeviation"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearBiasModification",
    "CylindricalGearCommonFlankMicroGeometry",
    "CylindricalGearFlankMicroGeometry",
    "CylindricalGearLeadModification",
    "CylindricalGearLeadModificationAtProfilePosition",
    "CylindricalGearMeshMicroGeometry",
    "CylindricalGearMeshMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometry",
    "CylindricalGearMicroGeometryBase",
    "CylindricalGearMicroGeometryDutyCycle",
    "CylindricalGearMicroGeometryMap",
    "CylindricalGearMicroGeometryPerTooth",
    "CylindricalGearProfileModification",
    "CylindricalGearProfileModificationAtFaceWidthPosition",
    "CylindricalGearSetMicroGeometry",
    "CylindricalGearSetMicroGeometryDutyCycle",
    "CylindricalGearToothMicroGeometry",
    "CylindricalGearTriangularEndModification",
    "CylindricalGearTriangularEndModificationAtOrientation",
    "DrawDefiningGearOrBoth",
    "GearAlignment",
    "LeadFormReliefWithDeviation",
    "LeadModificationForCustomer102CAD",
    "LeadReliefSpecificationForCustomer102",
    "LeadReliefWithDeviation",
    "LeadSlopeReliefWithDeviation",
    "LinearCylindricalGearTriangularEndModification",
    "MeasuredMapDataTypes",
    "MeshAlignment",
    "MeshedCylindricalGearFlankMicroGeometry",
    "MeshedCylindricalGearMicroGeometry",
    "MicroGeometryLeadToleranceChartView",
    "MicroGeometryViewingOptions",
    "ModificationForCustomer102CAD",
    "ParabolicCylindricalGearTriangularEndModification",
    "ProfileFormReliefWithDeviation",
    "ProfileModificationForCustomer102CAD",
    "ProfileReliefSpecificationForCustomer102",
    "ProfileReliefWithDeviation",
    "ProfileSlopeReliefWithDeviation",
    "ReliefWithDeviation",
    "SingleCylindricalGearTriangularEndModification",
    "TotalLeadReliefWithDeviation",
    "TotalProfileReliefWithDeviation",
)
