import pandas as pd

from pathological.resources_utils import resource_path


def grab_csv_path(dataset_name: str) -> str:
    return resource_path(f"datasets/{dataset_name}/challenges.csv")


def grab_dataset_dataframe(dataset_name: str) -> pd.DataFrame:
    return pd.read_csv(grab_csv_path(dataset_name), index_col="challenge_id")
