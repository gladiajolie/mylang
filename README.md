# mylang

A custom programming language built from scratch in Python, including a lexer, parser, and interpreter.

## Overview
mylang is a learning project where I'm building an interpreted programming language from the ground up — no libraries for parsing, just raw Python handling tokenization, parsing, and execution.

## Features Implemented
- Control flow (if/else, loops)
- Boolean logic
- Comments
- Negative numbers
- Lists
- String concatenation

## How It Works
The project follows the standard interpreter pipeline:
1. **Lexer** (`lexer.py`) — converts raw source code into tokens
2. **Parser** (`myparser.py`) — turns tokens into an abstract syntax tree (AST)
3. **Interpreter** (`interpreter.py`) — walks the AST and executes the program

## Usage
Replace `program.txt` with the path to a mylang source file.

## Built With
- Python

## What I'm Learning
Building this project from scratch to understand how programming languages actually work under the hood — tokenization, parsing, and execution — rather than just using existing ones.

## Status
Actively in development — more features being added.
