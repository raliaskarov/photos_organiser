# Photos Organizer

Simple tool to copy paste photos and videos from one folder to the other, sorting it by year/month in the way

## Moving photos from iPAD

 Step 1 — Mount the iPad

  On Linux, use ifuse (requires libimobiledevice + ifuse):

```
  sudo mkdir -p /mnt/ipad
  ifuse /mnt/ipad
```

  If not installed:
```
  sudo pacman -S ifuse libimobiledevice   # Arch
```
  or
```
  sudo apt install ifuse libimobiledevice-utils  # Debian/Ubuntu
```

  iPad photos are under /mnt/ipad/DCIM/.

  ---
  Step 2 — Run the script

  Copy :
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

  ---
  Step 3 — Unmount
```
  fusermount -u /mnt/ipad
```

