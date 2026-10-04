"""ATMOS WG1000 local WebSocket client."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from pyatmos_wg1000.client import AtmosClient
from pyatmos_wg1000.feed import AtmosFeed, InfoFeed, ValueStore
from pyatmos_wg1000.i18n import LanguageCatalog
from pyatmos_wg1000.protocol.pages import INFO_PAGE_POLL_INTERVAL, parse_pages_js_hod16_intervals

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    __version__ = version("py-atmos-wg1000")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "INFO_PAGE_POLL_INTERVAL",
    "AtmosClient",
    "AtmosFeed",
    "InfoFeed",
    "LanguageCatalog",
    "ValueStore",
    "__version__",
    "parse_pages_js_hod16_intervals",
]
