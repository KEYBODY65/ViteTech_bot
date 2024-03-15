from environs import Env
from dataclasses import dataclass


@dataclass
class KEY:
    key: str


@dataclass
class SETTINGS:
    key: KEY


def get_key(path):
    env = Env()
    env.read_env(path)

    return SETTINGS(
        key=env.str('KEY'),
    )


print()

