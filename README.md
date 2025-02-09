# s/Math + AI/ Reasoning in LLMs

![a demonstration of the sed puzzle](imgs/image.png)

This repository contains starter code in Python for PreCog's recruitment tasks. For more details, check the task doc.

# Documentation
## ``schema.py``
We define the data scheme using [Pydantic](https://docs.pydantic.dev/latest/) in ``schema.py``. This prevents any data validation problems. For the most part, you can treat it as a regular Python class that you can read from/write into JSON strings. We perform some basic validation checks to prevent invalid data being processed.
## ``utils.py``
- ``read_problem_folder()``/``read_solution_folder()``: Reads the corresponding JSON files and loads them as Python objects using Pydantic.
- ``write_problem_folder()``/``write_solution_folder()``:
Writes the problems/solutions to JSON files and saves them in the provided path.
- ``validate_solutions()``:
Takes in the problems and the provided solutions, and validates if the provided solution is correct for the given problem.

## ``baseline.py``
We implement a simple baseline that searches through the solution space until the empty string is reached. This is provided so that performance of LLM can be compared with traditional methods. You are free to improve it.

## Compilation and Execution
To compile and run the `generate.cpp` file, use the following command:
```sh
g++ -std=c++17 -I /opt/homebrew/include generate.cpp -o generate
```
After compilation, you can execute the program by running:
```sh
./generate
```

## Problem Levels and Classification
The problems are categorized into different difficulty levels based on the following scheme:

- **Level 0**: Problem IDs 1-13, 88-93
- **Level 1**: Problem IDs 14-33
- **Level 2**: Problem IDs 34-45, 94-100
- **Level 3**: Problem IDs 46-64
- **Level 4**: Problem IDs 65-80
- **Level 5**: Problem IDs 81-87

## Directory Structure
- **sample-data/puzzles/**: Contains all the problem statements.
- **sample-data/solutions/**: Contains the corresponding solutions for the problems.
- **testing/helpful_debugging**: A debugging script that was useful during development.
- **testing/test_case_generate_wrong**: Identifies cases where the validator was malfunctioning by applying transitions that were not possible on a given string.

