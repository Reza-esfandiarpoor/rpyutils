import json
import random
import string
from pathlib import Path

pardir = Path(__file__).parent.joinpath("data_files")

with pardir.joinpath("names.json").open("r") as f:
    NAMES = json.load(f)


with pardir.joinpath("adjectives.json").open("r") as f:
    ADJECTIVES = json.load(f)


def generate(n=1, t="n"):
    assert t in ["n", "a"]
    assert n > 0
    if t == "n":
        curr_list = NAMES
    else:
        curr_list = ADJECTIVES

    if n == 1:
        return random.choice(curr_list)
    else:
        others_ = list()
        if n > len(curr_list):
            others_ = [
                "".join([random.choice(string.ascii_uppercase) for _ in range(10)])
                for _ in range(n - len(curr_list))
            ]

        return random.sample(curr_list, k=min(len(curr_list), n)) + others_
