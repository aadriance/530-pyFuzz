# 530-pyFuzz

pyfuzz is a project from a software engineering class in college.  The goal was to write a tool to help debug programs to help understand how advanced tooling works.

This tool was functional at the time of completion.  While not a very useful tool, it was a great learning experience.

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
