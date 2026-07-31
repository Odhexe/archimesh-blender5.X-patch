# Archimesh Blender 5.x Compatibility Patch

This patch fixes missing parameter panels in Archimesh 1.2.5 when used with Blender 5.x.

## Problem

After creating a Room, Door, Window or other Archimesh object, the parameter panel never appears.

Instead, only this message is shown:

> Use Properties panel (N) to define parms

Selecting the object still does not show any editable properties.

---

## Cause

Archimesh checks whether an object is an Archimesh object using code like:

```python
if 'RoomGenerator' in obj:
```

Blender 5.x changed the behavior of CollectionProperty.

The expression above now returns False even when:

```python
len(obj.RoomGenerator) == 1
```

As a result:

- Room panel never appears
- Door panel never appears
- Window panel never appears
- Window Panel editor never appears

---

## Solution

Replace checks like:

```python
if 'RoomGenerator' in obj:
```

with

```python
if hasattr(obj, "RoomGenerator") and len(obj.RoomGenerator) > 0:
```

and replace

```python
if 'RoomGenerator' not in obj:
```

with

```python
if not hasattr(obj, "RoomGenerator") or len(obj.RoomGenerator) == 0:
```

The included patcher performs these replacements automatically.

---

## Usage

Run:

```bash
python patch_archimesh.py
```

Restart Blender.

Done.

---

## Tested

- Blender 5.2
- Archimesh 1.2.5

Verified working for:

- Room
- Door
- Window
- Window Panel

---

## Backup

The patcher automatically creates `.bak` files before modifying anything.

---

## Disclaimer

This project is not affiliated with the official Archimesh project.

It is a compatibility patch for Blender 5.x.
