"""Stock WG1000 ``Pages.js`` poll-interval grammar.

The panel timer uses ``PrmID1s`` / ``PrmID5s`` / ``PrmID10s`` / ``PrmID30s``
attributes on HOD16 bindings. The Informace page also requests a full Info dump
every 1 s (every 5 s on other pages).
"""

from __future__ import annotations

import re
from collections.abc import Mapping

from pyatmos_wg1000.protocol.catalog import Hod16

# Stock UI bucket names → seconds (see ``TPages.Timer`` in Pages.js).
_BUCKET_SECONDS: Mapping[str, float] = {
    "PrmID1s": 1.0,
    "PrmID5s": 5.0,
    "PrmID10s": 10.0,
    "PrmID30s": 30.0,
}

_ATTR_HOD16 = re.compile(r"""Atribut\.(PrmID(?:1s|5s|10s|30s))\}?=["']\[\$\{HOD16\.([A-Z0-9_]+)\}\]["']""")
_TEPLOTY_DYNAMIC = re.compile(r"""HOD16\[`\$\{circName\}_TEPLOTY`\][\s\S]{0,400}?Atribut\.PrmID5s\}?=["']\[\$\{circID\}\]["']""")

_TEPLOTY = (
    Hod16.O1_TEPLOTY,
    Hod16.O2_TEPLOTY,
    Hod16.O3_TEPLOTY,
    Hod16.O4_TEPLOTY,
    Hod16.TUV_TEPLOTY,
)

# Informace-page cadence from ``TPages.Timer`` (``T_1s`` + ``I_Req``).
INFO_PAGE_POLL_INTERVAL: float = 1.0


def parse_pages_js_hod16_intervals(source: str) -> dict[Hod16, float]:
    """Return each ``HOD16`` local → poll interval in seconds.

    When the same register appears in more than one bucket, the shortest
    interval wins. Dynamic set-temp bindings (``circID`` → ``*_TEPLOTY``)
    are treated as ``PrmID5s``. Unknown ``HOD16`` names are ignored.

    Args:
        source: Decompressed ``Pages.js`` text from the gateway UI bundle.
    """
    best: dict[Hod16, float] = {}

    def _note(local: Hod16, interval: float) -> None:
        previous = best.get(local)
        if previous is None or interval < previous:
            best[local] = interval

    for match in _ATTR_HOD16.finditer(source):
        bucket = match.group(1)
        name = match.group(2)
        if name not in Hod16.__members__:
            continue
        _note(Hod16[name], _BUCKET_SECONDS[bucket])

    if _TEPLOTY_DYNAMIC.search(source):
        for local in _TEPLOTY:
            _note(local, 5.0)

    return best


__all__ = [
    "INFO_PAGE_POLL_INTERVAL",
    "parse_pages_js_hod16_intervals",
]
