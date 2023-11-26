import sys
from collections import OrderedDict

import pprint

import cookiecutter

MIN_COOKIECUTTER_VERSION = "2.1"
MIN_PYTHON_VERSION = "3.9"
if sys.version < MIN_PYTHON_VERSION:
    print(
        f"Please use a newer version of python (current: {sys.version}, minimum_required: "
        f"{MIN_PYTHON_VERSION})"
    )

if cookiecutter.__version__ < MIN_COOKIECUTTER_VERSION:
    print(
        f"Please upgrade cookiecutter (pip install --upgrade cookiecutter) Current version: "
        f"{cookiecutter.__version__}, minimum required: {MIN_COOKIECUTTER_VERSION}"
    )
    raise SystemExit(1)

context: OrderedDict = {{cookiecutter}}
print("\nCreating a repo with context:")
pprint.pprint(dict(context))
