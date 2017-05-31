# 530-pyFuzz

## Requirements
pip install redbaron

## Usage
**python pyFuzz.py** <python_file_to_fuzz> <number_of_runs> **"**[**int** | **string** | **file:**<input_file> | **static:**\<arg>]**,** ...**"**

The program can fuzz arguments/inputs that are command line ints, command line strings, or input files.

int denotes integer argument to fuzz

string denotes string argument to fuzz

static:<arg> denotes argument that will not be fuzzed

file:<filename> denotes an input file to be fuzzed

Example run: python pyFuzz.py test.py 6 "string, file:input.txt, int, int, static:23"
