#!/usr/bin/env python3
"""
Build release artifacts in dist/:

  senior-design-review.zip  — upload to claude.ai (Customize > Skills > Add).
                              The skill folder sits at the zip root, and the
                              description is shortened to claude.ai's upload limit.
  senior-design-review.skill — same contents; the extension Claude apps show a
                              "Save skill" button for.

The plugin itself (Claude Code) keeps the full description in SKILL.md, which
triggers the skill more reliably.

    python3 scripts/build_release.py
"""
import pathlib
import re
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "senior-design-review"
DIST = ROOT / "dist"
NAME = "senior-design-review"

SHORT_DESCRIPTION = (
    "Senior product-designer review of a live web app on desktop and mobile: "
    "measured metrics plus critique of hierarchy, type, spacing, colour, states "
    "and identity. Use for design reviews."
)
assert len(SHORT_DESCRIPTION) <= 200, len(SHORT_DESCRIPTION)

SKIP = {"__pycache__", ".DS_Store"}


def main() -> None:
    DIST.mkdir(exist_ok=True)
    skill_md = (SKILL / "SKILL.md").read_text()
    quoted = '"' + SHORT_DESCRIPTION.replace('"', '\\"') + '"'
    short_md, n = re.subn(r"(?m)^description: .*$", lambda _: f"description: {quoted}", skill_md, count=1)
    assert n == 1, "frontmatter description not found"

    zip_path = DIST / f"{NAME}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            if f.is_dir() or any(part in SKIP for part in f.parts):
                continue
            arc = f"{NAME}/{f.relative_to(SKILL).as_posix()}"
            if f.name == "SKILL.md" and f.parent == SKILL:
                z.writestr(arc, short_md)
            else:
                z.write(f, arc)
    shutil.copyfile(zip_path, DIST / f"{NAME}.skill")
    print(f"built {zip_path} and {NAME}.skill ({zip_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
