# backy-py

a simple backup tool

![logo](logo.png)

## Features

- Store different backups in different locations

- Backup a folder and one or more of its subfolders separately

- Delete old backups to save space without affecting more recent ones

## Installation

```
git clone https://git.teknik.io/aidenholmes/backr-py

cd backr-py

make install # installs to ~/.local/bin
```

## Usage

```
backr.py -s <source> -l <location> [-n|-c] [-w|-e <comment>]

restor.py -s <source> -l <location>

# Example:

backr.py -s /foo/bar -l /foo/backups -n -w
```

## Removal

```
cd backr-py

make uninstall # removes from ~/.local/bin

cd ..

rm -rf backr-py/
```

## Scheduling Backups with Cron

1. Add command with `crontab -e`

```
# add this to crontab:

@reboot /home/user/.local/bin/backr.py -s /foo/bar -l /foo/backups -n -w
```

2. Change `/foo/bar` to your folder and `/foo/backups` to your backup location

3. Change `@reboot` to your desired schedule

4. Change `/home/user/.local/bin/backr.py` to your backr.py path

5. Change `-n` to `-c` if you want to use compression
