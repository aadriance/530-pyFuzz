# 530-pyFuzz

## Requirements
pip install redbaron

## Usage
**python pyFuzz.py <python_file_to_fuzz> <number_of_runs> "[int | string | file:<input_file> ], ..."**

The program can fuzz arguments/inputs that are command line ints, command line strings, or input files.

Example run: python pyFuzz.py test.py 6 "string, file:input.txt, int, int"
