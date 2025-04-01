"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines._1358 import AbstractStator
    from mastapy._private.electric_machines._1359 import AbstractToothAndSlot
    from mastapy._private.electric_machines._1360 import CADConductor
    from mastapy._private.electric_machines._1361 import CADElectricMachineDetail
    from mastapy._private.electric_machines._1362 import CADFieldWindingSpecification
    from mastapy._private.electric_machines._1363 import CADMagnetDetails
    from mastapy._private.electric_machines._1364 import CADMagnetsForLayer
    from mastapy._private.electric_machines._1365 import CADRotor
    from mastapy._private.electric_machines._1366 import CADStator
    from mastapy._private.electric_machines._1367 import CADToothAndSlot
    from mastapy._private.electric_machines._1368 import CADWoundFieldSynchronousRotor
    from mastapy._private.electric_machines._1369 import Coil
    from mastapy._private.electric_machines._1370 import CoilPositionInSlot
    from mastapy._private.electric_machines._1371 import CoolingDuctLayerSpecification
    from mastapy._private.electric_machines._1372 import CoolingDuctShape
    from mastapy._private.electric_machines._1373 import (
        CoreLossBuildFactorSpecificationMethod,
    )
    from mastapy._private.electric_machines._1374 import CoreLossCoefficients
    from mastapy._private.electric_machines._1375 import CutoutShape
    from mastapy._private.electric_machines._1376 import DoubleLayerWindingSlotPositions
    from mastapy._private.electric_machines._1377 import DQAxisConvention
    from mastapy._private.electric_machines._1378 import Eccentricity
    from mastapy._private.electric_machines._1379 import ElectricMachineDesignBase
    from mastapy._private.electric_machines._1380 import ElectricMachineDetail
    from mastapy._private.electric_machines._1381 import (
        ElectricMachineDetailInitialInformation,
    )
    from mastapy._private.electric_machines._1382 import (
        ElectricMachineElectromagneticAndThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1383 import ElectricMachineGroup
    from mastapy._private.electric_machines._1384 import (
        ElectricMachineMechanicalAnalysisMeshingOptions,
    )
    from mastapy._private.electric_machines._1385 import ElectricMachineMeshingOptions
    from mastapy._private.electric_machines._1386 import (
        ElectricMachineMeshingOptionsBase,
    )
    from mastapy._private.electric_machines._1387 import ElectricMachineSetup
    from mastapy._private.electric_machines._1388 import ElectricMachineSetupBase
    from mastapy._private.electric_machines._1389 import (
        ElectricMachineThermalMeshingOptions,
    )
    from mastapy._private.electric_machines._1390 import ElectricMachineType
    from mastapy._private.electric_machines._1391 import FieldWindingSpecification
    from mastapy._private.electric_machines._1392 import FieldWindingSpecificationBase
    from mastapy._private.electric_machines._1393 import FillFactorSpecificationMethod
    from mastapy._private.electric_machines._1394 import FluxBarriers
    from mastapy._private.electric_machines._1395 import FluxBarrierOrWeb
    from mastapy._private.electric_machines._1396 import FluxBarrierStyle
    from mastapy._private.electric_machines._1397 import GeneralElectricMachineMaterial
    from mastapy._private.electric_machines._1398 import (
        GeneralElectricMachineMaterialDatabase,
    )
    from mastapy._private.electric_machines._1399 import HairpinConductor
    from mastapy._private.electric_machines._1400 import (
        HarmonicLoadDataControlExcitationOptionForElectricMachineMode,
    )
    from mastapy._private.electric_machines._1401 import (
        IndividualConductorSpecificationSource,
    )
    from mastapy._private.electric_machines._1402 import (
        InteriorPermanentMagnetAndSynchronousReluctanceRotor,
    )
    from mastapy._private.electric_machines._1403 import InteriorPermanentMagnetMachine
    from mastapy._private.electric_machines._1404 import (
        IronLossCoefficientSpecificationMethod,
    )
    from mastapy._private.electric_machines._1405 import MagnetClearance
    from mastapy._private.electric_machines._1406 import MagnetConfiguration
    from mastapy._private.electric_machines._1407 import MagnetData
    from mastapy._private.electric_machines._1408 import MagnetDesign
    from mastapy._private.electric_machines._1409 import MagnetForLayer
    from mastapy._private.electric_machines._1410 import MagnetisationDirection
    from mastapy._private.electric_machines._1411 import MagnetMaterial
    from mastapy._private.electric_machines._1412 import MagnetMaterialDatabase
    from mastapy._private.electric_machines._1413 import MotorRotorSideFaceDetail
    from mastapy._private.electric_machines._1414 import NonCADElectricMachineDetail
    from mastapy._private.electric_machines._1415 import NotchShape
    from mastapy._private.electric_machines._1416 import NotchSpecification
    from mastapy._private.electric_machines._1417 import (
        PermanentMagnetAssistedSynchronousReluctanceMachine,
    )
    from mastapy._private.electric_machines._1418 import PermanentMagnetRotor
    from mastapy._private.electric_machines._1419 import Phase
    from mastapy._private.electric_machines._1420 import RegionID
    from mastapy._private.electric_machines._1421 import ResultsLocationsSpecification
    from mastapy._private.electric_machines._1422 import Rotor
    from mastapy._private.electric_machines._1423 import RotorInternalLayerSpecification
    from mastapy._private.electric_machines._1424 import RotorSkewSlice
    from mastapy._private.electric_machines._1425 import RotorType
    from mastapy._private.electric_machines._1426 import SingleOrDoubleLayerWindings
    from mastapy._private.electric_machines._1427 import SlotSectionDetail
    from mastapy._private.electric_machines._1428 import Stator
    from mastapy._private.electric_machines._1429 import StatorCutoutSpecification
    from mastapy._private.electric_machines._1430 import StatorRotorMaterial
    from mastapy._private.electric_machines._1431 import StatorRotorMaterialDatabase
    from mastapy._private.electric_machines._1432 import SurfacePermanentMagnetMachine
    from mastapy._private.electric_machines._1433 import SurfacePermanentMagnetRotor
    from mastapy._private.electric_machines._1434 import SynchronousReluctanceMachine
    from mastapy._private.electric_machines._1435 import ToothAndSlot
    from mastapy._private.electric_machines._1436 import ToothSlotStyle
    from mastapy._private.electric_machines._1437 import ToothTaperSpecification
    from mastapy._private.electric_machines._1438 import (
        TwoDimensionalFEModelForAnalysis,
    )
    from mastapy._private.electric_machines._1439 import (
        TwoDimensionalFEModelForElectromagneticAnalysis,
    )
    from mastapy._private.electric_machines._1440 import (
        TwoDimensionalFEModelForMechanicalAnalysis,
    )
    from mastapy._private.electric_machines._1441 import UShapedLayerSpecification
    from mastapy._private.electric_machines._1442 import VShapedMagnetLayerSpecification
    from mastapy._private.electric_machines._1443 import WindingConductor
    from mastapy._private.electric_machines._1444 import WindingConnection
    from mastapy._private.electric_machines._1445 import WindingMaterial
    from mastapy._private.electric_machines._1446 import WindingMaterialDatabase
    from mastapy._private.electric_machines._1447 import Windings
    from mastapy._private.electric_machines._1448 import WindingsViewer
    from mastapy._private.electric_machines._1449 import WindingType
    from mastapy._private.electric_machines._1450 import WireSizeSpecificationMethod
    from mastapy._private.electric_machines._1451 import WoundFieldSynchronousMachine
    from mastapy._private.electric_machines._1452 import WoundFieldSynchronousRotor
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines._1358": ["AbstractStator"],
        "_private.electric_machines._1359": ["AbstractToothAndSlot"],
        "_private.electric_machines._1360": ["CADConductor"],
        "_private.electric_machines._1361": ["CADElectricMachineDetail"],
        "_private.electric_machines._1362": ["CADFieldWindingSpecification"],
        "_private.electric_machines._1363": ["CADMagnetDetails"],
        "_private.electric_machines._1364": ["CADMagnetsForLayer"],
        "_private.electric_machines._1365": ["CADRotor"],
        "_private.electric_machines._1366": ["CADStator"],
        "_private.electric_machines._1367": ["CADToothAndSlot"],
        "_private.electric_machines._1368": ["CADWoundFieldSynchronousRotor"],
        "_private.electric_machines._1369": ["Coil"],
        "_private.electric_machines._1370": ["CoilPositionInSlot"],
        "_private.electric_machines._1371": ["CoolingDuctLayerSpecification"],
        "_private.electric_machines._1372": ["CoolingDuctShape"],
        "_private.electric_machines._1373": ["CoreLossBuildFactorSpecificationMethod"],
        "_private.electric_machines._1374": ["CoreLossCoefficients"],
        "_private.electric_machines._1375": ["CutoutShape"],
        "_private.electric_machines._1376": ["DoubleLayerWindingSlotPositions"],
        "_private.electric_machines._1377": ["DQAxisConvention"],
        "_private.electric_machines._1378": ["Eccentricity"],
        "_private.electric_machines._1379": ["ElectricMachineDesignBase"],
        "_private.electric_machines._1380": ["ElectricMachineDetail"],
        "_private.electric_machines._1381": ["ElectricMachineDetailInitialInformation"],
        "_private.electric_machines._1382": [
            "ElectricMachineElectromagneticAndThermalMeshingOptions"
        ],
        "_private.electric_machines._1383": ["ElectricMachineGroup"],
        "_private.electric_machines._1384": [
            "ElectricMachineMechanicalAnalysisMeshingOptions"
        ],
        "_private.electric_machines._1385": ["ElectricMachineMeshingOptions"],
        "_private.electric_machines._1386": ["ElectricMachineMeshingOptionsBase"],
        "_private.electric_machines._1387": ["ElectricMachineSetup"],
        "_private.electric_machines._1388": ["ElectricMachineSetupBase"],
        "_private.electric_machines._1389": ["ElectricMachineThermalMeshingOptions"],
        "_private.electric_machines._1390": ["ElectricMachineType"],
        "_private.electric_machines._1391": ["FieldWindingSpecification"],
        "_private.electric_machines._1392": ["FieldWindingSpecificationBase"],
        "_private.electric_machines._1393": ["FillFactorSpecificationMethod"],
        "_private.electric_machines._1394": ["FluxBarriers"],
        "_private.electric_machines._1395": ["FluxBarrierOrWeb"],
        "_private.electric_machines._1396": ["FluxBarrierStyle"],
        "_private.electric_machines._1397": ["GeneralElectricMachineMaterial"],
        "_private.electric_machines._1398": ["GeneralElectricMachineMaterialDatabase"],
        "_private.electric_machines._1399": ["HairpinConductor"],
        "_private.electric_machines._1400": [
            "HarmonicLoadDataControlExcitationOptionForElectricMachineMode"
        ],
        "_private.electric_machines._1401": ["IndividualConductorSpecificationSource"],
        "_private.electric_machines._1402": [
            "InteriorPermanentMagnetAndSynchronousReluctanceRotor"
        ],
        "_private.electric_machines._1403": ["InteriorPermanentMagnetMachine"],
        "_private.electric_machines._1404": ["IronLossCoefficientSpecificationMethod"],
        "_private.electric_machines._1405": ["MagnetClearance"],
        "_private.electric_machines._1406": ["MagnetConfiguration"],
        "_private.electric_machines._1407": ["MagnetData"],
        "_private.electric_machines._1408": ["MagnetDesign"],
        "_private.electric_machines._1409": ["MagnetForLayer"],
        "_private.electric_machines._1410": ["MagnetisationDirection"],
        "_private.electric_machines._1411": ["MagnetMaterial"],
        "_private.electric_machines._1412": ["MagnetMaterialDatabase"],
        "_private.electric_machines._1413": ["MotorRotorSideFaceDetail"],
        "_private.electric_machines._1414": ["NonCADElectricMachineDetail"],
        "_private.electric_machines._1415": ["NotchShape"],
        "_private.electric_machines._1416": ["NotchSpecification"],
        "_private.electric_machines._1417": [
            "PermanentMagnetAssistedSynchronousReluctanceMachine"
        ],
        "_private.electric_machines._1418": ["PermanentMagnetRotor"],
        "_private.electric_machines._1419": ["Phase"],
        "_private.electric_machines._1420": ["RegionID"],
        "_private.electric_machines._1421": ["ResultsLocationsSpecification"],
        "_private.electric_machines._1422": ["Rotor"],
        "_private.electric_machines._1423": ["RotorInternalLayerSpecification"],
        "_private.electric_machines._1424": ["RotorSkewSlice"],
        "_private.electric_machines._1425": ["RotorType"],
        "_private.electric_machines._1426": ["SingleOrDoubleLayerWindings"],
        "_private.electric_machines._1427": ["SlotSectionDetail"],
        "_private.electric_machines._1428": ["Stator"],
        "_private.electric_machines._1429": ["StatorCutoutSpecification"],
        "_private.electric_machines._1430": ["StatorRotorMaterial"],
        "_private.electric_machines._1431": ["StatorRotorMaterialDatabase"],
        "_private.electric_machines._1432": ["SurfacePermanentMagnetMachine"],
        "_private.electric_machines._1433": ["SurfacePermanentMagnetRotor"],
        "_private.electric_machines._1434": ["SynchronousReluctanceMachine"],
        "_private.electric_machines._1435": ["ToothAndSlot"],
        "_private.electric_machines._1436": ["ToothSlotStyle"],
        "_private.electric_machines._1437": ["ToothTaperSpecification"],
        "_private.electric_machines._1438": ["TwoDimensionalFEModelForAnalysis"],
        "_private.electric_machines._1439": [
            "TwoDimensionalFEModelForElectromagneticAnalysis"
        ],
        "_private.electric_machines._1440": [
            "TwoDimensionalFEModelForMechanicalAnalysis"
        ],
        "_private.electric_machines._1441": ["UShapedLayerSpecification"],
        "_private.electric_machines._1442": ["VShapedMagnetLayerSpecification"],
        "_private.electric_machines._1443": ["WindingConductor"],
        "_private.electric_machines._1444": ["WindingConnection"],
        "_private.electric_machines._1445": ["WindingMaterial"],
        "_private.electric_machines._1446": ["WindingMaterialDatabase"],
        "_private.electric_machines._1447": ["Windings"],
        "_private.electric_machines._1448": ["WindingsViewer"],
        "_private.electric_machines._1449": ["WindingType"],
        "_private.electric_machines._1450": ["WireSizeSpecificationMethod"],
        "_private.electric_machines._1451": ["WoundFieldSynchronousMachine"],
        "_private.electric_machines._1452": ["WoundFieldSynchronousRotor"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADFieldWindingSpecification",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "CADWoundFieldSynchronousRotor",
    "Coil",
    "CoilPositionInSlot",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "CutoutShape",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDesignBase",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineElectromagneticAndThermalMeshingOptions",
    "ElectricMachineGroup",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineSetupBase",
    "ElectricMachineThermalMeshingOptions",
    "ElectricMachineType",
    "FieldWindingSpecification",
    "FieldWindingSpecificationBase",
    "FillFactorSpecificationMethod",
    "FluxBarriers",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "GeneralElectricMachineMaterial",
    "GeneralElectricMachineMaterialDatabase",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "ResultsLocationsSpecification",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutoutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "TwoDimensionalFEModelForElectromagneticAnalysis",
    "TwoDimensionalFEModelForMechanicalAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
    "WoundFieldSynchronousRotor",
)
