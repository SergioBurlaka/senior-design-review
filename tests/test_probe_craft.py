"""
Regression tests for skills/senior-design-review/scripts/probe-craft.js.

Runs the probe in headless Chromium against small fixture pages whose defects
are known, at a phone and a desktop viewport, and checks that each detector
fires where it should and stays quiet where it should not.

    pip install playwright pytest && python -m playwright install chromium
    pytest tests
"""
import json
import pathlib

import pytest
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = (ROOT / "skills/senior-design-review/scripts/probe-craft.js").read_text()
FIXTURES = ROOT / "tests/fixtures"

PHONE = dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
DESKTOP = dict(viewport={"width": 1440, "height": 900})


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


def run(browser, fixture, ctx):
    context = browser.new_context(**ctx)
    page = context.new_page()
    page.goto((FIXTURES / fixture).as_uri())
    out = json.loads(page.evaluate(PROBE))
    context.close()
    return out


def test_all_sections_present(browser):
    out = run(browser, "craft-basic.html", PHONE)
    for key in ("gridDiscipline", "typeScale", "colourAndDepth", "dataViz",
                "genericnessTells", "useOfWidth", "inputErgonomics", "platform"):
        assert key in out, key


def test_grid_discipline_flags_off_grid_spacing(browser):
    g = run(browser, "craft-basic.html", PHONE)["gridDiscipline"]
    assert g["pctOn4pxGrid"] < 85
    assert any("13px" in s for s in g["offGridSamples"])


def test_body_size_is_weighted_by_text_not_by_headline(browser):
    t = run(browser, "craft-basic.html", PHONE)["typeScale"]
    assert t["bodySize"]["px"] == 16
    assert t["largestToBody"] == 2


def test_genericness_tells(browser):
    g = run(browser, "craft-basic.html", PHONE)["genericnessTells"]
    assert g["dominantDefaultFamily"].startswith("Inter")
    assert g["nestedCards"]["count"] == 1
    assert g["emojiAsIcons"]["count"] >= 1
    assert g["purpleBlueGradients"] == 1


def test_input_ergonomics_on_phone(browser):
    i = run(browser, "craft-basic.html", PHONE)["inputErgonomics"]
    assert any("weight" in s for s in i["under16pxFont"])
    assert any(f["type"] == "number" and f["inputmode"] is None for f in i["numericFields"])


def test_stretched_mobile_column_only_on_desktop(browser):
    assert run(browser, "craft-basic.html", DESKTOP)["useOfWidth"]["stretchedMobileColumn"] is True
    assert run(browser, "craft-basic.html", PHONE)["useOfWidth"]["stretchedMobileColumn"] is False


def test_pure_black_page_detected(browser):
    assert run(browser, "craft-basic.html", PHONE)["colourAndDepth"]["pageIsPureBlack"] is True


def test_invisible_progress_track_detected_and_visible_one_ignored(browser):
    d = run(browser, "craft-dataviz.html", DESKTOP)["dataViz"]
    assert d["invisibleTracks"]["count"] == 1


def test_clipped_svg_tick_label_detected(browser):
    d = run(browser, "craft-dataviz.html", DESKTOP)["dataViz"]
    assert d["clippedSvgText"]["samples"] == ["12000"]
