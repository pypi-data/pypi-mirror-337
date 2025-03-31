#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
from typing import Any, Optional

try:
    # noinspection PyUnresolvedReferences
    import tomllib
except ImportError:
    # noinspection PyUnresolvedReferences
    import tomli as tomllib


def get_values(cfg: dict[str, Any]) -> Optional[list[str]]:
    try:
        return  cfg['build']['targets']['wheel']['hooks']['pyside']['folders']
    except KeyError:
        return cfg['build']['hooks']['pyside']['folders']


def get_project_folders() -> tuple[str, Optional[list[str]]]:
    """ Extract hatch-pyside config from pyproject.toml or hatch.toml """
    name = None
    try:
        with open('pyproject.toml', 'rb') as fd:
            json = tomllib.load(fd)
            name = json['project']['name']
            return name, get_values(json['tool']['hatch'])
    except KeyError:
        if name is None:
            raise
        try:
            with open('hatch.toml', 'rb') as fd:
                return name, get_values(tomllib.load(fd))
        except (OSError, KeyError):
            return name, None
