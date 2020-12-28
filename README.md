# trailmap

### Project Status

[![Coverage Status](https://coveralls.io/repos/github/CNERG/trailmap/badge.svg?branch=main)](https://coveralls.io/github/CNERG/trailmap?branch=main) 
[![CircleCI](https://circleci.com/gh/CNERG/trailmap.svg?style=shield)](https://circleci.com/gh/CNERG/trailmap) 
![GitHub issues](https://img.shields.io/github/issues/cnerg/trailmap)
![GitHub pull requests](https://img.shields.io/github/issues-pr/cnerg/trailmap)
[![Cyclus Users Group](https://img.shields.io/badge/Cyclus%20Users%20Group-Join-orange)](https://groups.google.com/g/cyclus-users)

This tool takes a Cyclus input file and conducts acquisition pathway analysis on the facilities specified.

## Dependencies

* Python 3
* [Cyclus](https://github.com/cyclus/cyclus)

Follow installation instructions from [Cyclus](https://github.com/cyclus/cyclus).

* [NetworkX](https://networkx.github.io/)

run `pip install --user networkx`

Other Python packages which you may or may not already have installed:

* numpy
* matplotlib
* more_itertools

To install or confirm install of these additional packages, run

`pip install --user numpy matplotlib more_itertools`

### Recommended Packages

In addition to Cyclus, it is strongly recommended that the user install [Cycamore](https://github.com/cyclus/cycamore)

## Installation

run `python -m pip install . --user`

## Usage

From the top-level directory,

`python scripts/main.py /path/to/inputfile`
