"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.geometry_modeller_link._223 import (
        BaseGeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._224 import (
        GearTipRadiusClashTest,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._225 import (
        GeometryModellerAngleDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._226 import (
        GeometryModellerCountDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._227 import (
        GeometryModellerDesignInformation,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._228 import (
        GeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._229 import (
        GeometryModellerDimensions,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._230 import (
        GeometryModellerDimensionType,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._231 import (
        GeometryModellerLengthDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._232 import (
        GeometryModellerSettings,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._233 import (
        GeometryModellerUnitlessDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._234 import (
        GeometryTypeForComponentImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._235 import MeshRequest
    from mastapy._private.nodal_analysis.geometry_modeller_link._236 import (
        MeshRequestResult,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._237 import (
        ProfileFromImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._238 import (
        RepositionComponentDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.geometry_modeller_link._223": [
            "BaseGeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._224": [
            "GearTipRadiusClashTest"
        ],
        "_private.nodal_analysis.geometry_modeller_link._225": [
            "GeometryModellerAngleDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._226": [
            "GeometryModellerCountDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._227": [
            "GeometryModellerDesignInformation"
        ],
        "_private.nodal_analysis.geometry_modeller_link._228": [
            "GeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._229": [
            "GeometryModellerDimensions"
        ],
        "_private.nodal_analysis.geometry_modeller_link._230": [
            "GeometryModellerDimensionType"
        ],
        "_private.nodal_analysis.geometry_modeller_link._231": [
            "GeometryModellerLengthDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._232": [
            "GeometryModellerSettings"
        ],
        "_private.nodal_analysis.geometry_modeller_link._233": [
            "GeometryModellerUnitlessDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._234": [
            "GeometryTypeForComponentImport"
        ],
        "_private.nodal_analysis.geometry_modeller_link._235": ["MeshRequest"],
        "_private.nodal_analysis.geometry_modeller_link._236": ["MeshRequestResult"],
        "_private.nodal_analysis.geometry_modeller_link._237": ["ProfileFromImport"],
        "_private.nodal_analysis.geometry_modeller_link._238": [
            "RepositionComponentDetails"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BaseGeometryModellerDimension",
    "GearTipRadiusClashTest",
    "GeometryModellerAngleDimension",
    "GeometryModellerCountDimension",
    "GeometryModellerDesignInformation",
    "GeometryModellerDimension",
    "GeometryModellerDimensions",
    "GeometryModellerDimensionType",
    "GeometryModellerLengthDimension",
    "GeometryModellerSettings",
    "GeometryModellerUnitlessDimension",
    "GeometryTypeForComponentImport",
    "MeshRequest",
    "MeshRequestResult",
    "ProfileFromImport",
    "RepositionComponentDetails",
)
