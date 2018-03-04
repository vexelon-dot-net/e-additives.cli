# e-additives CLI

Brings food additives info to your console.

This is a command-line interface for [E-additives](https://github.com/vexelon-dot-net/e-additives.server) with a local database for faster results delivery.

# Installation

Requires Python `2.7` or `3.x`.

Run `make` or `pip install -r requirements.txt`.

# Setup

Make sure `ead.py` is executable.

    chmod +x ead.py

# Usage

Look up and additive by its E number.

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

Look up an additive by its E number and display infos in specified locale. Only English `en` and Bulgarian `bg` locales are currently supported.

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

Query by phrase matching. This will match all additives that have the `aspar` phrase in their data set.

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

```Please note that this is a hobby project. I SHALL NOT be held liable in case of any damages incurring from the usage of this data!```
