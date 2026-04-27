import json

def load_rules():
    with open("data/pet_care_rules.json", "r") as file:
        return json.load(file)

def get_guideline(pet_type, task):
    rules = load_rules()

    pet_type = pet_type.lower()
    task = task.lower()

    for rule in rules:
        if rule["pet_type"] == pet_type and rule["task"] == task:
            return rule["guideline"]

    return "No guideline found for this task yet."