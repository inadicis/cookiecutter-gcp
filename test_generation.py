import os
import pathlib
import random
import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter as cc_create_project

REPO_ROOT = Path(__file__).parent


@pytest.fixture()
def output_dir() -> Path:
    """Deletes the dir after the test if something was created"""
    path = REPO_ROOT / "generated_repos"
    if not path.exists():
        os.makedirs(path)
    yield path


@pytest.mark.parametrize(
    "database",
    [
        "No DB",
        "MongoDB (pymongo)",
        "MongoDB (beanie)",
        # "MongoDB (motor.io)", # TODO motor io broken
        # "SQL (sqlalchemy)(niy)"
    ],
)
@pytest.mark.parametrize("use_socketio", ["No", "Yes"])
@pytest.mark.parametrize("use_graphql", ["No", "Yes"])
# @pytest.mark.parametrize("use_socketio", ["No"])
@pytest.mark.parametrize("use_gcp_pubsub", ["No", "Yes"])
# @pytest.mark.parametrize("use_gcp_pubsub", ["No"])
@pytest.mark.parametrize("use_server_side_rendering", ["No", "Yes"])
@pytest.mark.parametrize("use_auth0", ["No", "Yes"])
def test_generation(
    output_dir: Path,
    database: str,
    use_socketio: str,
    use_gcp_pubsub: str,
    use_server_side_rendering: str,
    use_auth0: str,
    use_graphql: str,
):
    # requires all possible dependencies
    # (run `pip install -r all_possible_requirements.txt` before)

    cc_context = {
        "project_name": f"my_project_{random.randint(0, 10 ** 50)}",
        "database": database,
        "use_socketio": use_socketio,
        "use_gcp_pubsub": use_gcp_pubsub,
        "use_server_side_rendering": use_server_side_rendering,
        "use_auth0": use_auth0,
        "use_graphql": use_graphql,
        "__run_post_gen_tests": True,
    }
    path_str = cc_create_project(
        str(REPO_ROOT),
        no_input=True,
        extra_context=cc_context,
        output_dir=str(output_dir),
        keep_project_on_failure=True,
    )
    new_project_path = pathlib.Path(path_str)
    assert (new_project_path / "socket_client.py").exists() == (use_socketio == "Yes")
    assert not (new_project_path / "pyproject.toml.jinja").exists()
    assert (new_project_path / "pyproject.toml").exists()

    if new_project_path.exists():
        shutil.rmtree(new_project_path, onerror=change_read_only)


def change_read_only(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error? (read only file)
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise
