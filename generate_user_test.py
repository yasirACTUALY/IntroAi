"""Generate a recipe-similarity user test.

The script selects groups of 4 random recipes from a dataset. For each group,
one recipe is chosen as the primary recipe and the user is asked to select the
most similar recipe among the remaining three. Results are stored in JSON.
"""
# %%  
from __future__ import annotations
import argparse
import csv
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence

import load_dataset


TITLE_KEYS = ("title", "name", "recipe_name", "recipe")


@dataclass
class TestRound:
	primary_recipe: Dict[str, Any]
	options: List[Dict[str, Any]]
	chosen_index: int
	correct_index: int | None
	is_correct: bool | None

def recipe_label(recipe: Dict[str, Any]) -> str:
	for key in TITLE_KEYS:
		value = recipe.get(key)
		if value:
			return str(value)
	return "<unknown recipe>"


def pick_group(recipes: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
	if len(recipes) < 4:
		raise ValueError("Need at least 4 recipes to create a test group.")
	return random.sample(list(recipes), 4)


def get_user_choice(options: Sequence[Dict[str, Any]]) -> int:
	print("Choose the recipe most similar to the primary recipe:")
	for idx, option in enumerate(options, start=1):
		print(f"  {idx}. {recipe_label(option)}")

	while True:
		choice = input("Enter 1-3: ").strip()
		if choice.isdigit() and 1 <= int(choice) <= 3:
			return int(choice) - 1
		print("Invalid choice. Please enter 1, 2, or 3.")


def compute_similarity_score(primary: Dict[str, Any], candidate: Dict[str, Any]) -> float | None:
	primary_text = str(primary.get("ingredients", "")).lower()
	candidate_text = str(candidate.get("ingredients", "")).lower()
	if not primary_text or not candidate_text:
		return None

	primary_tokens = set(primary_text.replace(",", " ").split())
	candidate_tokens = set(candidate_text.replace(",", " ").split())
	if not primary_tokens or not candidate_tokens:
		return None

	return len(primary_tokens & candidate_tokens) / len(primary_tokens | candidate_tokens)


def find_best_match(primary: Dict[str, Any], options: Sequence[Dict[str, Any]]) -> int | None:
	scores = [compute_similarity_score(primary, option) for option in options]
	valid_scores = [score for score in scores if score is not None]
	if not valid_scores:
		return None

	best_score = max(valid_scores)
	for idx, score in enumerate(scores):
		if score == best_score:
			return idx
	return None


def run_test(recipes: Sequence[Dict[str, Any]], rounds: int, output: Path) -> List[TestRound]:
	results: List[TestRound] = []

	for round_number in range(1, rounds + 1):
		print(f"\nRound {round_number}/{rounds}")
		group = pick_group(recipes)
		primary_index = random.randrange(4)
		primary = group[primary_index]
		options = [recipe for idx, recipe in enumerate(group) if idx != primary_index]

		print(f"Primary recipe: {recipe_label(primary)}")
		chosen_index = get_user_choice(options)
		correct_index = find_best_match(primary, options)
		is_correct = None if correct_index is None else chosen_index == correct_index

		if correct_index is not None:
			print(f"Correct answer: {correct_index + 1}. {recipe_label(options[correct_index])}")
			print("Result:", "Correct" if is_correct else "Incorrect")
		else:
			print("No similarity signal found; stored user response only.")

		results.append(
			TestRound(
				primary_recipe=primary,
				options=options,
				chosen_index=chosen_index,
				correct_index=correct_index,
				is_correct=is_correct,
			)
		)

	with output.open("w", encoding="utf-8") as f:
		json.dump([asdict(item) for item in results], f, indent=2, ensure_ascii=False)

	return results


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Generate a user recipe similarity test.")
	parser.add_argument("-n", "--rounds", type=int, default=10, help="Number of rounds to run")
	parser.add_argument(
		"-o",
		"--output",
		type=Path,
		default=Path("user_test_results.json"),
		help="Output file for stored results",
	)
	return parser.parse_args()

def turn_data_to_a_dict(data):
    """Convert the dataset to a dictionary format."""
    if data is None:
        return None
    result = {}
    for idx, row in data.iterrows():
        result[idx] = row.to_dict()
    return result


def main() -> None:
	args = parse_args()
	recipes = turn_data_to_a_dict(load_dataset.data)
	if len(recipes) < 4:
		raise ValueError("Dataset must contain at least 4 recipes.")
	run_test(recipes, args.rounds, args.output)


if __name__ == "__main__":
	recipes = turn_data_to_a_dict(load_dataset.data)
	run_test(recipes, 3, Path('user_test_results.json'))



# %%
