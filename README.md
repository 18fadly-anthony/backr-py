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

1. ~~change license to apache2~~

2. indentation / various small issues found in emacs

3. take args using module

4. do not except keybord inturrupt in if name

5. create ~/backrs automatically

6. get slug comment some other way than just rejecting “/“

7. prefer args to prompting the user

8. use separate variables for backr_location

9. restor —clean feature to remove old backups from backup list

10. use Makefile to compile files in installation

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
