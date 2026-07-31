# Archimesh Blender 5.x Compatibility Patch

A compatibility patch for **Archimesh 1.2.5** that restores the missing parameter panels when using **Blender 5.x**.

## Problem

On Blender 5.x, creating Archimesh objects such as:

- Room
- Door
- Window
- Window Panel

only displays:

> Use Properties panel (N) to define parms

Selecting the object does not show any editable parameters.

---

## Cause

Archimesh checks whether an object is an Archimesh object using code such as:

```python
if 'RoomGenerator' in obj:
```

In Blender 5.x this check no longer works correctly for `CollectionProperty`, causing the editor panels to remain hidden.

---

## What this patch does

The patch replaces the old compatibility checks with Blender 5.x compatible ones.

It automatically:

- Creates backups (`.bak`)
- Patches all supported generator checks
- Saves the modified files

---

# Installation

## Step 1

Download **Archimesh 1.2.5**.

## Step 2

Extract the ZIP.

Example:

```
add-on-archimesh-v1.2.5/
```

## Step 3

Place `patch_archimesh.py` inside the extracted folder.

Example:

```
add-on-archimesh-v1.2.5/
│
├── patch_archimesh.py
├── achm_room_maker.py
├── achm_door_maker.py
├── ...
```

## Step 4

Edit the `ROOT` variable inside `patch_archimesh.py` if necessary.

Example:

```python
ROOT = Path(r"D:\Games\add-on-archimesh-v1.2.5")
```

## Step 5

Run:

```bash
python patch_archimesh.py
```

The script will patch the addon and create backup files.

## Step 6

Compress the patched folder back into a ZIP.

Make sure the ZIP contains the addon files directly.

Correct:

```
add-on-archimesh-v1.2.5.zip
│
├── __init__.py
├── achm_room_maker.py
├── achm_door_maker.py
└── ...
```

Not:

```
add-on-archimesh-v1.2.5.zip
└── add-on-archimesh-v1.2.5
    ├── __init__.py
```

## Step 7

Open Blender.

Go to:

```
Edit
→ Preferences
→ Extensions
→ ▼
→ Install from Disk
```

Select the patched ZIP.

Enable Archimesh.

Done.

---

# Tested

- Blender 5.2
- Archimesh 1.2.5

Verified working:

- ✅ Room
- ✅ Door
- ✅ Window
- ✅ Window Panel

---

# Backups

The patcher creates `.bak` files before modifying any source file.

---

# Disclaimer

This project is an unofficial compatibility patch and is not affiliated with the official Archimesh project.

If the issue is fixed in a future official release, this patch should no longer be necessary.

## Credits

Compatibility patch developed by **Mr0dh**.
