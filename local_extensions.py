from typing import Any

from cookiecutter.utils import simple_filter
from jinja2.ext import Extension


class TruthyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters['bool'] = is_truthy


def is_truthy(v: str | Any) -> bool:
    if not isinstance(v, str):
        return bool(v)

    return not any(
        [
            v == "",
            v == "2",
            "false" in v.casefold(),
            v.casefold().startswith("n"),
            v.isdigit() and int(v) == 0,
        ]
    )
