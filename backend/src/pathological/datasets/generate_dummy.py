import random
import uuid

import pandas as pd

from pathological.datasets.grab_util import grab_csv_path


def generate_dummy():
    dummy_records = [
        {"challenge_id": uuid.uuid4(),
         "correct_answer": "death",
         "possible_answers": ";".join(["death", "double death", "triple death"]),
         "image_path": random.choice(["path1.jpeg", "path2.png"])
         }
        for _ in range(1000)
    ]
    dataframe = pd.DataFrame.from_records(dummy_records)
    dataframe.to_csv(grab_csv_path("dummy"))


if __name__ == "__main__":
    generate_dummy()
