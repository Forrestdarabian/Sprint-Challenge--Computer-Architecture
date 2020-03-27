#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()
if len(sys.argv) != 2:
    print("ERROR: must have file name")
    sys.exit(1)

cpu.load()
cpu.run()
