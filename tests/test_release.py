"""The skill's frontmatter must parse as YAML both in the plugin and in the claude.ai release zip."""
import pathlib
import subprocess
import sys
import zipfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def frontmatter(text: str) -> dict:
    return yaml.safe_load(text.split("---")[1])


def test_plugin_frontmatter():
    fm = frontmatter((ROOT / "skills/senior-design-review/SKILL.md").read_text())
    assert fm["name"] == "senior-design-review"
    assert 0 < len(fm["description"]) <= 1024


def test_release_zip_frontmatter_and_layout():
    subprocess.run([sys.executable, "-I", str(ROOT / "scripts/build_release.py")], check=True)
    with zipfile.ZipFile(ROOT / "dist/senior-design-review.zip") as z:
        names = z.namelist()
        assert all(n.startswith("senior-design-review/") for n in names)
        fm = frontmatter(z.read("senior-design-review/SKILL.md").decode())
    assert fm["name"] == "senior-design-review"
    assert len(fm["description"]) <= 200
