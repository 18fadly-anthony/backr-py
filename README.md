# backy-py

a simple backup tool

![logo](logo.png)

## Example: backuping and and restoring a directory's contents with backr

[![asciicast](https://asciinema.org/a/sNBDRobpOUBwTHNr2G4xBEIUM.svg)](https://asciinema.org/a/sNBDRobpOUBwTHNr2G4xBEIUM)

## Features

- Store different backups in different locations

- Backup a folder and one or more of its subfolders separately

- Delete old backups to save space without affecting more recent ones

## ToDo

1. ~~create ~/backrs automatically~~

2. get slug comment some other way than just rejecting “/“

3. prefer args to prompting the user

4. use separate variables for backr_location

5. restor —clean feature to remove old backups from backup list

6. use Makefile to compile files in installation

7. do less in main() (keep in mind during other todos)

## Installation

```
git clone https://github.com/aidenholmes/backr-py

cd backr-py
```

put `backr.py` and `restor.py` in PATH, eg:

```
ln -s ~/backr-py/backr.py ~/.local/bin

ln -s ~/backr-py/restor.py ~/.local/bin
```

## Usage

```
cd /foo/bar

backr.py # to backup

restor.py # to restore
```

## Removal

Remove backr.py and restor.py from PATH then delete the repository
