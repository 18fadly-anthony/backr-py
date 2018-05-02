# backy-py

### [backr](https://github.com/aidenholmes/backr) rewritten in python

## ToDo

1. Finish restor.py

## Features

- Store different backups in different locations

- Backup a folder and one or more of its subfolders separately

- Delete old backups to save space without affecting more recent ones

## Installation

```
git clone https://github.com/aidenholmes/backr-py

cd backr-py

ln -s $(pwd)"/backr.py" ~/.local/bin/

# optional make ~/backrs for default backup location

mkdir ~/backrs
```

## Usage

```
cd /foo/bar

backr.py
```

## Removal

```
rm ~/.local/bin/backr.py

cd backr-py

cd ..

rm -rf backr-py

```
