#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

program = []

if (len(sys.argv)) != 2:
    print("Please pass the second file name")
    print("usage: python3 fileio.py <second_file_name.py>")
    sys.exit()

try:
    with open(sys.argv[1]) as f:
        for line in f:
            possible_num = line[:line.find('#')]
            if possible_num == '':
                continue
            integer = int(possible_num, 2)
            program.append(integer)
except FileNotFoundError:
    print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
    sys.exit()

# print('program', program)

cpu = CPU()

cpu.load(program)
cpu.run()
