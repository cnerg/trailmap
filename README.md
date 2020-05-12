# trailmap

This tool takes a Cyclus input file and conducts acquisition pathway analysis on the facilities specified.

## Dependencies

* Python 3
* [Cyclus](https://github.com/cyclus/cyclus)
* [Cycamore](https://github.com/cyclus/cycamore)
* [NetworkX](https://networkx.github.io/)

Follow installation instructions from [Cyclus](https://github.com/cyclus/cyclus) and [Cycamore](https://github.com/cyclus/cycamore).

Install NetworkX

`python -m install networkx`

## Installation

run `python -m pip install -e . --user`

## Usage

From the top-level directory,

`python scripts/main.py /path/to/inputfile`
