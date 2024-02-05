import attrs

from pathological.app_config.env_tool import get_or_default

DUMMY_DATASET_NAME = "dummy"


@attrs.define
class AppParameters:
    dataset_name: str


APP_PARAMETERS = AppParameters(
    dataset_name=get_or_default("GAME_DATASET_NAME", DUMMY_DATASET_NAME)
)
