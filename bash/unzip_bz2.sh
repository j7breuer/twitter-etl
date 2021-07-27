#!/bin/bash

# Recursively unzip all bz2 file types from a directory
find . -iname '*.bz2' -exec sh -c 'bzip2 -d "${0%.*}" "$0"' '{}' ';'
