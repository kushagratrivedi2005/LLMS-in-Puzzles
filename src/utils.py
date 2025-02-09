import os
from pathlib import Path
import schema
import json
import logging

import pydantic

def read_problem_folder(path=Path("puzzles")):
    """Opens all problems at the folder and reads them using Pydantic"""
    problems = {}
    for file_path in path.iterdir():
        problem_data = json.loads(file_path.read_text())
        try:
            problem = schema.Problem(**problem_data)
            problems[problem.problem_id] = problem
        except pydantic.ValidationError as e:
            logging.warning(f"Validation error while processing {file_path}! skipping...", exc_info=True)
    return problems

def read_solution_folder(path=Path("solutions")):
    """Opens all solutions at the folder and reads them using Pydantic"""
    solutions = {}
    for file_path in path.iterdir():
        solution_data = json.loads(file_path.read_text())
        try:
            solution = schema.Solution(**solution_data)
            solutions[solution.problem_id] = solution
        except pydantic.ValidationError as e:
            logging.warning(f"Validation error while processing {file_path}! skipping... ", exc_info=True)
    return solutions

def write_problem_folder(problems, path=Path("puzzles")):
    path.mkdir(exist_ok=True)

    for problem_id, problem in problems.items():
        logging.info(f"Saving problem {problem_id}...")
        with open(path / f"{problem_id}.json", 'w') as f:
            f.write(problem.json())

def write_solution_folder(solutions, path=Path("../sample-data/solutions")):
    path.mkdir(exist_ok=True)

    for problem_id, solution in solutions.items():
        logging.info("=====================================================")
        logging.info(f"Saving solution to problem {problem_id}...")
        with open(path / f"{problem_id}.json", 'w') as f:
            f.write(solution.json())

def validate_solutions(problems, solutions):
    """
    Validates solutions by checking if they result in an empty string at the end of their transitions.
    """
    for problem_id in problems:
        logging.info("=====================================================")
        if problem_id not in solutions:
            logging.warning(f"Problem {problem_id} does not have a solution, skipping...")
            continue

        problem = problems[problem_id]
        solution = solutions[problem_id]

        transitions = problem.transitions
        current = problem.initial_string

        for step in solution.solution:
            if step >= len(transitions):
                logging.warning(f"Invalid step number {step} found! skipping problem...")
                break
            from_pattern = transitions[step].src
            to_pattern = transitions[step].tgt
            current = current.replace(from_pattern, to_pattern, 1)
            logging.info(f"Pattern: {from_pattern} -> {to_pattern}, String: {current}")

        if current != '':
            logging.warning(f"Problem {problem_id} has an invalid solution!")
        else:
            logging.info(f"Problem {problem_id} has a valid solution!")
