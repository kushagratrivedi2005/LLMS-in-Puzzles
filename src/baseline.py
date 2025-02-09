import os
import json
import time
from utils import read_problem_folder, write_solution_folder
from schema import Solution
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def bfs(problem, time_limit=5):
    initial = problem.initial_string
    transitions = problem.transitions

    queue = [(initial, 0)]
    operation = {initial: -1}  # Map current string to the transition index used
    parent = {initial: None}  # Map current string to its parent string
    start_time = time.time()  # Record the start time

    while queue:
        current_string, steps = queue.pop(0)

        if time.time() - start_time > time_limit:
            return None

        # Check if the target string is empty
        if current_string == "":
            solution = []
            while current_string is not None:
                operation_index = operation[current_string]
                if operation_index != -1:
                    solution.append(operation_index)
                current_string = parent[current_string]

            return solution[::-1]  # Reverse to get the correct order

        # Process all transitions
        for i, transition in enumerate(transitions):
            src = transition.src
            tgt = transition.tgt

            pos = current_string.find(src) if src else 0
            if pos != -1:
                new_string = current_string[:pos] + tgt + current_string[pos + len(src):]

                if new_string not in operation:
                    operation[new_string] = i  # Store the transition index
                    parent[new_string] = current_string
                    queue.append((new_string, steps + 1))

    return None  # No solution found

def main():
    # Load the generated puzzles
    problems = read_problem_folder()

    solutions = {}
    for problem in problems.values():
        logging.info("=====================================================")
        solution = bfs(problem)
        if solution is not None:
            solutions[problem.problem_id] = Solution(
                problem_id = problem.problem_id,
                solution = solution
            )
            logging.info(f"Solution found for puzzle {problem.problem_id}")
        else:
            logging.info(f"Baseline exceedes time limit for puzzle {problem.problem_id}")

    write_solution_folder(solutions)

if __name__ == "__main__":
    main()
