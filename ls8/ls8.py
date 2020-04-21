#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# NORMAL state of affairs is this line
# filename = sys.argv[1]

# BUT we want to debug, so we have to hard set it.
filename = "f:\\Dev\\js\\LAMBDA\\CS\\Unit 2\\Week 3\\Computer-Architecture\\ls8\\examples\\print8.ls8"

cpu = CPU()

cpu.load(filename)
cpu.run() 