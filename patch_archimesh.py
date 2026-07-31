from pathlib import Path
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parent


required_files = [
    "__init__.py",
    "achm_room_maker.py",
    "achm_door_maker.py",
]

missing = [f for f in required_files if not (ROOT / f).exists()]

if missing:
    print("ERROR")
    print("This script must be placed inside the extracted Archimesh addon folder.\n")
    print("Missing required files:")
    for f in missing:
        print(" -", f)

    print("\nCurrent folder:")
    print(ROOT)
    input("\nPress Enter to exit...")
    sys.exit(1)


REPLACEMENTS = [

    # Room
    (
        re.compile(r"if\s+'RoomGenerator'\s+in\s+(\w+)\s*:"),
        r"if hasattr(\1, 'RoomGenerator') and len(\1.RoomGenerator) > 0:"
    ),

    (
        re.compile(r"if\s+'RoomGenerator'\s+not\s+in\s+(\w+)\s*:"),
        r"if not hasattr(\1, 'RoomGenerator') or len(\1.RoomGenerator) == 0:"
    ),

    # Door
    (
        re.compile(r"if\s+'DoorObjectGenerator'\s+in\s+(\w+)\s*:"),
        r"if hasattr(\1, 'DoorObjectGenerator') and len(\1.DoorObjectGenerator) > 0:"
    ),

    (
        re.compile(r"if\s+'DoorObjectGenerator'\s+not\s+in\s+(\w+)\s*:"),
        r"if not hasattr(\1, 'DoorObjectGenerator') or len(\1.DoorObjectGenerator) == 0:"
    ),

    # Window
    (
        re.compile(r"if\s+'WindowObjectGenerator'\s+in\s+(\w+)\s*:"),
        r"if hasattr(\1, 'WindowObjectGenerator') and len(\1.WindowObjectGenerator) > 0:"
    ),

    (
        re.compile(r"if\s+'WindowObjectGenerator'\s+not\s+in\s+(\w+)\s*:"),
        r"if not hasattr(\1, 'WindowObjectGenerator') or len(\1.WindowObjectGenerator) == 0:"
    ),

    # Window Panel
    (
        re.compile(r"if\s+'WindowPanelGenerator'\s+in\s+(\w+)\s*:"),
        r"if hasattr(\1, 'WindowPanelGenerator') and len(\1.WindowPanelGenerator) > 0:"
    ),

    (
        re.compile(r"if\s+'WindowPanelGenerator'\s+not\s+in\s+(\w+)\s*:"),
        r"if not hasattr(\1, 'WindowPanelGenerator') or len(\1.WindowPanelGenerator) == 0:"
    ),
]

# ----------------------------------------------------------
# poll() replacement
# ----------------------------------------------------------

POLL_PATTERN = re.compile(
    r"""if\s+o\s+is\s+None:\s*
\s*return\s+False\s*
\s*if\s+'([A-Za-z]+Generator)'\s+not\s+in\s+o:\s*
\s*return\s+False\s*
\s*else:\s*
\s*return\s+True""",
    re.MULTILINE | re.VERBOSE
)

def poll_replacement(match):
    prop = match.group(1)

    return f"""if o is None:
            return False
        try:
            return hasattr(o, "{prop}") and len(o.{prop}) > 0
        except Exception:
            return False"""

# ----------------------------------------------------------
# Patch
# ----------------------------------------------------------

patched_files = 0
patched_lines = 0

print("=" * 60)
print("Archimesh Blender 5.x Compatibility Patcher")
print("=" * 60)
print()

for pyfile in ROOT.rglob("*.py"):

    original = pyfile.read_text(encoding="utf8")

    modified = original

    modified = POLL_PATTERN.sub(poll_replacement, modified)

    for regex, replacement in REPLACEMENTS:
        modified, count = regex.subn(replacement, modified)
        patched_lines += count

    if modified != original:

        backup = pyfile.with_suffix(pyfile.suffix + ".bak")

        if not backup.exists():
            shutil.copy2(pyfile, backup)

        pyfile.write_text(modified, encoding="utf8")

        patched_files += 1

        print(f"✓ Patched {pyfile.name}")

print()
print("=" * 60)
print(f"Files patched : {patched_files}")
print(f"Changes made  : {patched_lines}")
print("=" * 60)

if patched_files == 0:
    print("\nNo changes were necessary.")
else:
    print("\nSuccess!")
    print("You can now zip the addon folder and install it in Blender.")
    print("Backup files (.bak) were created automatically.")

input("\nPress Enter to exit...")