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
cd /foo/bar

backr.py # to backup

restor.py # to restore
```

## Removal

```
cd backr-py

make uninstall # removes from ~/.local/bin

cd ..

rm -rf backr-py/
```

## Scheduling Backups with Cron

1. Backup directory manually to set backr location

```
cd /foo/bar

backr.py
```

2. Add command with `crontab -e`

```
# add this to crontab:

@reboot cd /foo/bar; /home/user/.local/bin/backr.py -n -w
```

3. Change `@reboot` to your desired schedule

4. Change `/home/user/.local/bin/backr.py` to your backr.py path

5. Change `-n` to `-c` if you want to use compression
