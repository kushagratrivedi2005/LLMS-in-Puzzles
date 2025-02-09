import logging

from utils import read_problem_folder, read_solution_folder, validate_solutions

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Loading the generated puzzles
    problems = read_problem_folder()
    # Loading the solution to the puzzles
    solutions = read_solution_folder()
    # Validate the solution
    validate_solutions(problems, solutions)

if __name__ == "__main__":
    main()
