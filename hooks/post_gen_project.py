import json
import logging
import os
import pathlib
import pprint
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
import pkg_resources

import cookiecutter


class MissingDependency(Exception):
    ...


repo_path = pathlib.Path().absolute()


context: OrderedDict = {{ cookiecutter }}
versions = {
    "python": sys.version,
    "cookiecutter": cookiecutter.__version__,
    "dists": [str(d) for d in pkg_resources.working_set]
}
with open(repo_path / "cookiecutter" / "cc_context.jsonl", "a") as f:
    pprint.pprint(dict(context))
    json.dump(context, f)
    f.write("\n")
    json.dump(versions, f)


print("\n" + "=" * 100)
print("Validating template variables...")

project_slug = "{{ cookiecutter.__project_slug }}"

if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]+$", project_slug):
    print(f"ERROR: {project_slug} is not a valid Python module name!")
    sys.exit(1)

db_option = "{{ cookiecutter.database }}"

print("\n" + "=" * 100)
print("Removing extra files...")

REMOVE_PATHS = [
    "tests/test_filterable_documents.py",
    ".ruff_cache",
    {% if not cookiecutter.database | bool %}
    "src/documents.py",
    "src/config/database.py",
    "tests/additional_documents.py",
    "tests/test_database.py",
    {% endif %}
    {% if not cookiecutter.use_auth0 | bool %}
    "src/authentication.py",
    "tests/test_authentication.py",
    "src/config/fake_jwks.py",
    "docs/auth0.md",
    "docs/auth0_get_token.png",
    {% endif %}
    {% if not cookiecutter.use_server_side_rendering | bool %}
    "templates/example.html",
    "templates/partials/",
    {% endif %}
    {% if not cookiecutter.__keep_internal_readmes | bool %}
    "tests/readme.md",
    "docs/readme.md",
    "deployment/readme.md",
    "src/readme.md",
    {% endif %}
    {% if not cookiecutter.use_socketio | bool %}
    "src/config/sockets.py",
    "src/event_handlers.py",
    "socket_client.py",
    "tests/test_sockets.py",
    "src/templates/wsdocs.html.jinja",
    "docs/asyncapi.yaml",
    {% if not cookiecutter.use_server_side_rendering | bool %}
    "src/templates",
    {% endif %}
    {% endif %}
    {% if not cookiecutter.use_gcp_pubsub | bool %}
    "src/serializers/pubsub_serializers.py",
    "src/routes/pubsub_routes.py",
    "tests/test_pubsub.py",
    {% endif %}
    {% if cookiecutter.__linter != "ruff" %}
    "tests/test_formatting.py",
    {% endif %}
    {% if not cookiecutter.use_gradio | bool%}
    "src/gui.py",
    {% endif %}
    {% if not cookiecutter.use_graphql | bool %}
    "src/graphql",
        "src/config/graphql.py",
    "tests/test_graphql_query.py",
    {% endif %}
]


for relative_path in REMOVE_PATHS:
    # try deleting with and without jinja extension
    for suffix in ["", ".jinja", ".jinja2"]:
        path = repo_path / (relative_path + suffix)
        if not path.exists():
            print(f"Couldnt delete, Not found: {path} ")
            continue

        if path.is_dir():
            shutil.rmtree(path)
            print(f" - Directory {path} deteled")
        else:
            path.unlink()
            print(f" - File {path} deleted")
        break


# Rename all jinja files to their actual type
jinja_exceptions = [
    "wsdocs.html.jinja",
]
for root, dirs, files in os.walk("."):
    root_path = pathlib.Path(root)
    for file in files:
        for suffix in [".jinja", ".jinja2"]:
            if file.endswith(suffix) and not file in jinja_exceptions:
                (root_path / file).rename( root_path / file.removesuffix(suffix))

print("\n" + "=" * 100)
print("Initializing git Repo...")

git_executable = shutil.which("git")
if not git_executable:
    raise MissingDependency("Please make sure git is installed on your machine!")

subprocess.call([git_executable, "init"])
subprocess.call([git_executable, "branch", "-m", "main"])
subprocess.call([git_executable, "add", "*"])
subprocess.call([git_executable, "commit", "-m", "Initial commit"])
print("\n" + "=" * 100)

print("Running linter...")

ruff_executable = shutil.which("ruff")
if not ruff_executable:
    raise MissingDependency("Please make sure ruff is installed on your machine!")
subprocess.call([ruff_executable, "check", "--fix", "--fix-only", "."])

black_executable = shutil.which("black")
if not black_executable:
    raise MissingDependency("Please make sure black is installed on your machine!")
subprocess.call([black_executable, "."])
subprocess.call([git_executable, "add", "*"])
subprocess.call([git_executable, "commit", "-m", "Commit after ruff autofix"])

# ruff_exit_code = subprocess.call(["ruff", "check", "."])
# if ruff_exit_code != 0:
#     sys.exit(ruff_exit_code)

# requires installing all possible dependencies (requirements.txt) before
{% if cookiecutter.__run_post_gen_tests | bool -%}
import pytest
pytest_exit_code = pytest.main()
if pytest_exit_code != 0:
    sys.exit(pytest_exit_code)
{%- endif %}

print("\n" + "=" * 100)
print(f"Repo creation finished at {repo_path}.\nSee next steps in new projects' "
      f"cookiecutter/TODOs.md")
print("-" * 100 + "\n")
