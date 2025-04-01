"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility._1665 import AcousticWeighting
    from mastapy._private.math_utility._1666 import AlignmentAxis
    from mastapy._private.math_utility._1667 import Axis
    from mastapy._private.math_utility._1668 import CirclesOnAxis
    from mastapy._private.math_utility._1669 import ComplexMatrix
    from mastapy._private.math_utility._1670 import ComplexPartDisplayOption
    from mastapy._private.math_utility._1671 import ComplexVector
    from mastapy._private.math_utility._1672 import ComplexVector3D
    from mastapy._private.math_utility._1673 import ComplexVector6D
    from mastapy._private.math_utility._1674 import CoordinateSystem3D
    from mastapy._private.math_utility._1675 import CoordinateSystemEditor
    from mastapy._private.math_utility._1676 import CoordinateSystemForRotation
    from mastapy._private.math_utility._1677 import CoordinateSystemForRotationOrigin
    from mastapy._private.math_utility._1678 import DataPrecision
    from mastapy._private.math_utility._1679 import DegreeOfFreedom
    from mastapy._private.math_utility._1680 import DynamicsResponseScalarResult
    from mastapy._private.math_utility._1681 import DynamicsResponseScaling
    from mastapy._private.math_utility._1682 import Eigenmode
    from mastapy._private.math_utility._1683 import Eigenmodes
    from mastapy._private.math_utility._1684 import EulerParameters
    from mastapy._private.math_utility._1685 import ExtrapolationOptions
    from mastapy._private.math_utility._1686 import FacetedBody
    from mastapy._private.math_utility._1687 import FacetedSurface
    from mastapy._private.math_utility._1688 import FourierSeries
    from mastapy._private.math_utility._1689 import GenericMatrix
    from mastapy._private.math_utility._1690 import GriddedSurface
    from mastapy._private.math_utility._1691 import HarmonicValue
    from mastapy._private.math_utility._1692 import InertiaTensor
    from mastapy._private.math_utility._1693 import MassProperties
    from mastapy._private.math_utility._1694 import MaxMinMean
    from mastapy._private.math_utility._1695 import ComplexMagnitudeMethod
    from mastapy._private.math_utility._1696 import MultipleFourierSeriesInterpolator
    from mastapy._private.math_utility._1697 import Named2DLocation
    from mastapy._private.math_utility._1698 import PIDControlUpdateMethod
    from mastapy._private.math_utility._1699 import Quaternion
    from mastapy._private.math_utility._1700 import RealMatrix
    from mastapy._private.math_utility._1701 import RealVector
    from mastapy._private.math_utility._1702 import ResultOptionsFor3DVector
    from mastapy._private.math_utility._1703 import RotationAxis
    from mastapy._private.math_utility._1704 import RoundedOrder
    from mastapy._private.math_utility._1705 import SinCurve
    from mastapy._private.math_utility._1706 import SquareMatrix
    from mastapy._private.math_utility._1707 import StressPoint
    from mastapy._private.math_utility._1708 import TranslationRotation
    from mastapy._private.math_utility._1709 import Vector2DListAccessor
    from mastapy._private.math_utility._1710 import Vector6D
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility._1665": ["AcousticWeighting"],
        "_private.math_utility._1666": ["AlignmentAxis"],
        "_private.math_utility._1667": ["Axis"],
        "_private.math_utility._1668": ["CirclesOnAxis"],
        "_private.math_utility._1669": ["ComplexMatrix"],
        "_private.math_utility._1670": ["ComplexPartDisplayOption"],
        "_private.math_utility._1671": ["ComplexVector"],
        "_private.math_utility._1672": ["ComplexVector3D"],
        "_private.math_utility._1673": ["ComplexVector6D"],
        "_private.math_utility._1674": ["CoordinateSystem3D"],
        "_private.math_utility._1675": ["CoordinateSystemEditor"],
        "_private.math_utility._1676": ["CoordinateSystemForRotation"],
        "_private.math_utility._1677": ["CoordinateSystemForRotationOrigin"],
        "_private.math_utility._1678": ["DataPrecision"],
        "_private.math_utility._1679": ["DegreeOfFreedom"],
        "_private.math_utility._1680": ["DynamicsResponseScalarResult"],
        "_private.math_utility._1681": ["DynamicsResponseScaling"],
        "_private.math_utility._1682": ["Eigenmode"],
        "_private.math_utility._1683": ["Eigenmodes"],
        "_private.math_utility._1684": ["EulerParameters"],
        "_private.math_utility._1685": ["ExtrapolationOptions"],
        "_private.math_utility._1686": ["FacetedBody"],
        "_private.math_utility._1687": ["FacetedSurface"],
        "_private.math_utility._1688": ["FourierSeries"],
        "_private.math_utility._1689": ["GenericMatrix"],
        "_private.math_utility._1690": ["GriddedSurface"],
        "_private.math_utility._1691": ["HarmonicValue"],
        "_private.math_utility._1692": ["InertiaTensor"],
        "_private.math_utility._1693": ["MassProperties"],
        "_private.math_utility._1694": ["MaxMinMean"],
        "_private.math_utility._1695": ["ComplexMagnitudeMethod"],
        "_private.math_utility._1696": ["MultipleFourierSeriesInterpolator"],
        "_private.math_utility._1697": ["Named2DLocation"],
        "_private.math_utility._1698": ["PIDControlUpdateMethod"],
        "_private.math_utility._1699": ["Quaternion"],
        "_private.math_utility._1700": ["RealMatrix"],
        "_private.math_utility._1701": ["RealVector"],
        "_private.math_utility._1702": ["ResultOptionsFor3DVector"],
        "_private.math_utility._1703": ["RotationAxis"],
        "_private.math_utility._1704": ["RoundedOrder"],
        "_private.math_utility._1705": ["SinCurve"],
        "_private.math_utility._1706": ["SquareMatrix"],
        "_private.math_utility._1707": ["StressPoint"],
        "_private.math_utility._1708": ["TranslationRotation"],
        "_private.math_utility._1709": ["Vector2DListAccessor"],
        "_private.math_utility._1710": ["Vector6D"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
