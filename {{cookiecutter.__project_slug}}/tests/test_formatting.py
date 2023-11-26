import subprocess

import pytest

from src.config import BASE_DIR


@pytest.mark.asyncio
async def test_ruff_raises_no_warnings():

    exit_code = subprocess.call(["ruff", "check", str(BASE_DIR)])  # noqa: 603 607
    assert exit_code == 0
