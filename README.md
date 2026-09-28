# Photos Organizer

Simple tool to copy or move photos and videos from one folder to another, sorting them into `year/month` subfolders along the way.

## Options

| Option | Description |
|---|---|
| `--source`, `-s` | Source directory containing photos and videos (required) |
| `--dest`, `-d` | Destination base directory for the sorted files (required) |
| `--type`, `-t` | Which media to process: `photos`, `videos` or `both` (default: `both`) |
| `--move` | Move files instead of copying them |
| `--heic-to-jpeg` | Convert HEIC photos to JPEG instead of copying them as-is |

## Moving photos from iPad

### Step 1 — Mount the iPad

On Linux, use `ifuse` (requires `libimobiledevice` + `ifuse`):

```
sudo mkdir -p /mnt/ipad
ifuse /mnt/ipad
```

If not installed:

```
sudo pacman -S ifuse libimobiledevice          # Arch
```

or

```
sudo apt install ifuse libimobiledevice-utils  # Debian/Ubuntu
```

iPad photos are under `/mnt/ipad/DCIM/`.

---

### Step 2 — Run the script

Copy:

```
cd /{project_folder}
source env/bin/activate
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted
```

Move (removes from iPad after transfer):

```
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted --move
```

Move + convert HEIC to JPEG (common for iPhone/iPad photos):

```
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted --move --heic-to-jpeg
```

#### Choosing photos, videos or both

Use `--type` to process only one kind of media. Without it, both are processed.

Only photos:

```
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted --type photos
```

Only videos (moved off the iPad):

```
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted --type videos --move
```

Photos only, moved and converted to JPEG:

```
python organise_photos.py --source /mnt/ipad/DCIM --dest /mnt/external/photos_sorted --type photos --move --heic-to-jpeg
```

> Note: `--heic-to-jpeg` only affects photos, so it has no effect with `--type videos`.

---

### Step 3 — Unmount

```
fusermount -u /mnt/ipad
```
