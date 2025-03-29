PyFunLibs Ultimate Complete
Overview
SuperLib Ultimate Complete is a self-contained Python library that provides a wide range of functionalities without relying on external packages (except for a few built-in modules). It is designed for educational and demonstration purposes, offering various algorithms, system utilities, and an interactive command-line interface.

Features
Random Number Generation:
Uses a Linear Congruential Generator (LCG) to produce pseudo-random numbers. Supports generating both floating-point numbers (between 0 and 1) and random integers within a specified range.

Length Check:
Provides a simple function to determine the length of strings, lists, and any object that supports Python’s built-in len function.

Mathematical Operations:
Implements basic arithmetic operations (addition, subtraction, multiplication, division) as well as advanced operations such as exponentiation, square roots, factorials, and trigonometric functions (sine and cosine via Taylor series).

String Similarity Comparison:
Includes an implementation of the Levenshtein distance algorithm to compare two strings and calculates a similarity ratio based on the edit distance.

Sorting Algorithms:
Offers a variety of sorting methods, including:

Bubble Sort, Quick Sort, Insertion Sort, Selection Sort, Merge Sort, Heap Sort, Shell Sort, Counting Sort, Radix Sort, Gnome Sort, and Comb Sort.
Swap/Reverse Algorithm: Reverses the order of elements in a list (e.g., transforms [1,2,3,4,5,6,7] into [7,6,5,4,3,2,1]).
Colorful Output:
Uses ANSI escape codes to print colored text in the terminal.

System Information Retrieval:

Generates a simple hardware identifier (HWID) based on the current working directory, system platform, and Python version.
Simulates cookie retrieval by returning a fixed string.
Delay Function:
Provides a busy-waiting delay function for simple timing purposes (note that its precision is limited).

Command-Line Interface (CMD):
An interactive menu that allows users to test and demonstrate all of the library’s functionalities.

Extended Features & Macro Support:

Supports special markers in strings for dynamic content replacement:
\nt converts to a newline followed by a space.
%winver displays the Windows version.
%verx shows the Windows architecture (32-bit or 64-bit).
%getc: (e.g., %getc:C:) returns the free disk space (in gigabytes) for the specified drive.
%getfps: displays a placeholder FPS value.
An enhanced printf() function processes these markers before printing.
Allows defining custom macros using the $ prefix (e.g., $name), which can be updated with the define_macro() function.
Installation
To install the library, first package it and upload it to PyPI. Once published, you can install it using pip:

pip install SuperLibUltimateComplete