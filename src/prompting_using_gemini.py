import json
import requests
import time
import os

# Define paths
PUZZLE_FOLDER = os.path.join(os.path.dirname(__file__), "Puzzles")
SOLUTION_FOLDER = os.path.join(os.path.dirname(__file__), "Solutions")

# Ensure the solutions directory exists
os.makedirs(SOLUTION_FOLDER, exist_ok=True)

# Load a puzzle from JSON file
def load_puzzles(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [data] if isinstance(data, dict) else data

# Generate a Lookahead Prompt
def generate_prompt(problem):
    # Example to guide the model
    example_problem = {
        "problem_id": "001",
        "initial_string": "abcabc",
        "transitions": [
            {"src": "abc", "tgt": ""},
            {"src": "bc", "tgt": "c"}
        ]
    }

    example_solution = """
Example:
Problem ID: 001
Initial string: "abcabc"
Transitions:
0. "abc" → ""
1. "bc" → "c"

### Lookahead Strategy:
1. Identify which transitions can be applied at each step.
2. Predict the resulting string **before applying each transformation**.
3. Choose the transition that brings the string **closest to empty** in the fewest steps.

### Step-by-step reasoning:
1. The initial string is "abcabc".
2. Applying transition 0 ("abc" → ""), we predict the string will become "abc".
3. Applying transition 0 again, we predict the string will become "" (empty).
4. The optimal solution sequence is **[0, 0]**.

Final Answer (JSON format):
{
    "problem_id": "001",
    "solution": [0, 0]
}
""".strip()

    # Convert the current problem into text format
    transitions_text = "\n".join(
        f"{i}. \"{t['src']}\" → \"{t['tgt']}\""
        for i, t in enumerate(problem["transitions"])
    )

    lookahead_prompt = f"""
Solve the following problem using a **Lookahead Strategy** before providing the JSON output.

{example_solution}

Now solve this new problem:

Problem ID: {problem["problem_id"]}
Initial string: "{problem["initial_string"]}"
Transitions:
{transitions_text}

### Lookahead Strategy:
1. Identify possible transitions at each step.
2. **Predict** the resulting string **before applying any transformation**.
3. Select the transition that minimizes remaining transformations.
4. Repeat until the string becomes empty.

### Step-by-step reasoning:
1. Start with the initial string: "{problem["initial_string"]}".
2. Apply the lookahead approach to determine the best sequence.
3. Stop when the string is empty.

Final Answer (JSON format):
{{
    "problem_id": "{problem["problem_id"]}",
    "solution": [index1, index2, ...]  # Must be within 25 steps.
}}
""".strip()

    print("\n===== GENERATED LOOKAHEAD PROMPT =====\n")
    print(lookahead_prompt)
    print("\n======================================\n")

    return lookahead_prompt

# Call Gemini API
def call_gemini_api(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}

    response = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
    return response.json()

# Process all puzzles in the "Puzzles" folder
def run_experiments(api_key):
    puzzle_files = [f for f in os.listdir(PUZZLE_FOLDER) if f.endswith(".json")]

    for puzzle_file in puzzle_files:
        puzzle_path = os.path.join(PUZZLE_FOLDER, puzzle_file)
        puzzles = load_puzzles(puzzle_path)

        for puzzle in puzzles:
            prompt = generate_prompt(puzzle)  # Generate Lookahead prompt
            response = call_gemini_api(prompt, api_key)  # Get API response
            print(f"Raw response for problem {puzzle['problem_id']}: {response}")

            try:
                response_text = response["candidates"][0]["content"]["parts"][0]["text"]
                response_text = response_text.strip("```json").strip("``` ").strip()
                solution_data = json.loads(response_text)
            except (KeyError, json.JSONDecodeError, TypeError) as e:
                print(f"Failed to parse response for problem {puzzle['problem_id']} - {e}")
                solution_data = {"problem_id": puzzle["problem_id"], "solution": []}

            solution_file = os.path.join(SOLUTION_FOLDER, f"{puzzle['problem_id']}.json")
            with open(solution_file, "w") as f:
                json.dump(solution_data, f, indent=4)

            print(f"Solution saved: {solution_file}")
            time.sleep(1)  # Avoid hitting rate limits

# Usage Example
if __name__ == "__main__":
    API_KEY = os.getenv("GEMINI_API_KEY")  # Use environment variable for security
    run_experiments(API_KEY)
