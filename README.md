# e-additives CLI

Brings food additives info to your console.

This is a command-line interface for [E-additives](https://github.com/vexelon-dot-net/e-additives.server) using a local database for fast results delivery.

# Installation

Requires Python `2.7` or `3.x`.

## Packages

To install on **ArchLinux** from [AUR](https://aur.archlinux.org/packages/e-additives.cli) run:

    yaourt -S e-additives.cli

## Manual

Run `make` or `pip install -r requirements.txt`.

Download the `eadditives.sqlite3` database file from the [releases page](https://github.com/vexelon-dot-net/e-additives.cli/releases). 

Set the path to the database using an environment variable.

    export EAD_DB_PATH=<path>/eadditives.sqlite3

Alternatively you may pass the path to the database using the command line parameter `--db`.

Make sure `ead.py` is executable.

    chmod +x ead.py

# Usage

Look up an additive by its E number.

    ead.py 951

```
Code
	E 951
Name
	Aspartame
Category
	miscellaneous
Function
	sweetener
......
```

Look up an additive by its E number and display infos using a given locale. Only English `en` and Bulgarian `bg` locales are currently supported.

    ead.py -l bg 951
```
Code
	E 951
Name
	Aspartame
Category
	разни
Function
	подсладител
......
```

Simple text query.

    ead.py aspartame

Query by phrase matching. This will match all additives that have the `aspar` phrase in their data.

    ead.py aspar

Show all additive categories.

    ead.py -c

Query category infos.

    ead.py -c colors

Display help and options.

    ead.py -h

# License

[MIT License](LICENSE)

# Disclaimer

```Please note that E-additives is a hobby project. I SHALL NOT be held liable in case of any damages incurring from the usage of this data!```
