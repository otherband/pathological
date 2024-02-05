import os


def get_or_default(env_var_name: str, default_value: str) -> str:
    env_var = os.getenv(env_var_name)
    return env_var or default_value
