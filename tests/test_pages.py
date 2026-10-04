"""Pages.js PrmID bucket parsing for HOD16 poll cadence."""

from __future__ import annotations

from pathlib import Path

from pyatmos_wg1000.protocol import Hod16, parse_pages_js_hod16_intervals
from pyatmos_wg1000.protocol.pages import INFO_PAGE_POLL_INTERVAL

_FIXTURE = Path(__file__).parent / "fixtures" / "pages_circuit_schedule.js"


def test_parse_pages_js_assigns_stock_buckets() -> None:
    """Homepage temps are 30 s; regime/general/setpoints are 5 s."""
    source = _FIXTURE.read_text(encoding="utf-8")
    intervals = parse_pages_js_hod16_intervals(source)

    assert intervals[Hod16.O1_TEPLOTA] == 30.0
    assert intervals[Hod16.TUV_VLHKOST] == 30.0
    assert intervals[Hod16.O1_OBECNE] == 5.0
    assert intervals[Hod16.TUV_REZIM] == 5.0
    assert intervals[Hod16.O1_TEPLOTY] == 5.0
    assert intervals[Hod16.TUV_TEPLOTY] == 5.0
    assert intervals[Hod16.O1_TRVALY_REZIM] == 30.0


def test_parse_pages_js_keeps_shortest_interval_and_skips_unknown() -> None:
    """Duplicate bindings keep the faster bucket; unknown HOD16 names are ignored."""
    source = """
    <span ${Atribut.PrmID5s}="[${HOD16.O1_TEPLOTA}]"></span>
    <span ${Atribut.PrmID30s}="[${HOD16.O1_TEPLOTA}]"></span>
    <span ${Atribut.PrmID1s}="[${HOD16.NOT_A_REAL_REGISTER}]"></span>
    """
    intervals = parse_pages_js_hod16_intervals(source)
    assert intervals[Hod16.O1_TEPLOTA] == 5.0
    assert Hod16.O1_TEPLOTY not in intervals


def test_info_page_poll_interval_matches_informace_timer() -> None:
    """Stock Informace page asks for a dump every 1 s."""
    assert INFO_PAGE_POLL_INTERVAL == 1.0
