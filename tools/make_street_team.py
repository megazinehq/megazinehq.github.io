"""Zip the sticker sheets for the Street Team downloads. Rerun after any sticker sheet changes.
    python3 tools/make_street_team.py   # print/street-team/*.zip
"""
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
S, OUT = ROOT / "print" / "stickers", ROOT / "print" / "street-team"
OUT.mkdir(exist_ok=True)
for name, folder in [("megazine-stickers-black-and-white.zip", S), ("megazine-stickers-colour.zip", S / "color")]:
    with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(folder.glob("stickers-*.pdf")):
            z.write(f, f.name)
    print("wrote", (OUT / name).relative_to(ROOT))
