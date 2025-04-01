"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2546 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2547 import AlignmentMethod
    from mastapy._private.system_model.fe._2548 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2549 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2550 import AngleSource
    from mastapy._private.system_model.fe._2551 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2552 import BatchOperations
    from mastapy._private.system_model.fe._2553 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2554 import BearingNodeOption
    from mastapy._private.system_model.fe._2555 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2556 import BearingRacePosition
    from mastapy._private.system_model.fe._2557 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2558 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2559 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2560 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2561 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2562 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2563 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2564 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2565 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2566 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2567 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2568 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2569 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2570 import FEExportSettings
    from mastapy._private.system_model.fe._2571 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2572 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2573 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2574 import FEStiffnessTester
    from mastapy._private.system_model.fe._2575 import FESubstructure
    from mastapy._private.system_model.fe._2576 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2577 import FESubstructureNode
    from mastapy._private.system_model.fe._2578 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2579 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2580 import FESubstructureType
    from mastapy._private.system_model.fe._2581 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2582 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2583 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2584 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2585 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2586 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2587 import GearMeshingOptions
    from mastapy._private.system_model.fe._2588 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2589 import (
        IndependentMASTACreatedConstrainedNodes,
    )
    from mastapy._private.system_model.fe._2590 import (
        IndependentMASTACreatedConstrainedNodesWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2591 import (
        IndependentMASTACreatedRigidlyConnectedNodeGroup,
    )
    from mastapy._private.system_model.fe._2592 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2593 import LinkNodeSource
    from mastapy._private.system_model.fe._2594 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2595 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2596 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2597 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2598 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2599 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2600 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2601 import RaceBearingFE
    from mastapy._private.system_model.fe._2602 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2603 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2604 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2605 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2606 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2546": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2547": ["AlignmentMethod"],
        "_private.system_model.fe._2548": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2549": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2550": ["AngleSource"],
        "_private.system_model.fe._2551": ["BaseFEWithSelection"],
        "_private.system_model.fe._2552": ["BatchOperations"],
        "_private.system_model.fe._2553": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2554": ["BearingNodeOption"],
        "_private.system_model.fe._2555": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2556": ["BearingRacePosition"],
        "_private.system_model.fe._2557": ["ComponentOrientationOption"],
        "_private.system_model.fe._2558": ["ContactPairWithSelection"],
        "_private.system_model.fe._2559": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2560": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2561": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2562": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2563": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2564": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2565": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2566": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2567": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2568": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2569": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2570": ["FEExportSettings"],
        "_private.system_model.fe._2571": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2572": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2573": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2574": ["FEStiffnessTester"],
        "_private.system_model.fe._2575": ["FESubstructure"],
        "_private.system_model.fe._2576": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2577": ["FESubstructureNode"],
        "_private.system_model.fe._2578": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2579": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2580": ["FESubstructureType"],
        "_private.system_model.fe._2581": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2582": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2583": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2584": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2585": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2586": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2587": ["GearMeshingOptions"],
        "_private.system_model.fe._2588": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2589": ["IndependentMASTACreatedConstrainedNodes"],
        "_private.system_model.fe._2590": [
            "IndependentMASTACreatedConstrainedNodesWithSelectionComponents"
        ],
        "_private.system_model.fe._2591": [
            "IndependentMASTACreatedRigidlyConnectedNodeGroup"
        ],
        "_private.system_model.fe._2592": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2593": ["LinkNodeSource"],
        "_private.system_model.fe._2594": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2595": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2596": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2597": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2598": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2599": ["PerLinkExportOptions"],
        "_private.system_model.fe._2600": ["PerNodeExportOptions"],
        "_private.system_model.fe._2601": ["RaceBearingFE"],
        "_private.system_model.fe._2602": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2603": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2604": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2605": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2606": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "IndependentMASTACreatedConstrainedNodes",
    "IndependentMASTACreatedConstrainedNodesWithSelectionComponents",
    "IndependentMASTACreatedRigidlyConnectedNodeGroup",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
