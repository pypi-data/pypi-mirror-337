"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.databases._2005 import ConnectionState
    from mastapy._private.utility.databases._2006 import Database
    from mastapy._private.utility.databases._2007 import DatabaseConnectionSettings
    from mastapy._private.utility.databases._2008 import DatabaseKey
    from mastapy._private.utility.databases._2009 import DatabaseSettings
    from mastapy._private.utility.databases._2010 import NamedDatabase
    from mastapy._private.utility.databases._2011 import NamedDatabaseItem
    from mastapy._private.utility.databases._2012 import NamedKey
    from mastapy._private.utility.databases._2013 import (
        NetworkDatabaseConnectionSettingsItem,
    )
    from mastapy._private.utility.databases._2014 import SQLDatabase
    from mastapy._private.utility.databases._2015 import VersionUpdater
    from mastapy._private.utility.databases._2016 import VersionUpdaterSelectableItem
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.databases._2005": ["ConnectionState"],
        "_private.utility.databases._2006": ["Database"],
        "_private.utility.databases._2007": ["DatabaseConnectionSettings"],
        "_private.utility.databases._2008": ["DatabaseKey"],
        "_private.utility.databases._2009": ["DatabaseSettings"],
        "_private.utility.databases._2010": ["NamedDatabase"],
        "_private.utility.databases._2011": ["NamedDatabaseItem"],
        "_private.utility.databases._2012": ["NamedKey"],
        "_private.utility.databases._2013": ["NetworkDatabaseConnectionSettingsItem"],
        "_private.utility.databases._2014": ["SQLDatabase"],
        "_private.utility.databases._2015": ["VersionUpdater"],
        "_private.utility.databases._2016": ["VersionUpdaterSelectableItem"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConnectionState",
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "NetworkDatabaseConnectionSettingsItem",
    "SQLDatabase",
    "VersionUpdater",
    "VersionUpdaterSelectableItem",
)
