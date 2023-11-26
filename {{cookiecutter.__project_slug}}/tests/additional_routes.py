"""
Additionnal routes that are only added to the app when testing it automatically.
Useful for language / framework / tools testing.
"""
from typing import Annotated

from fastapi import APIRouter, Security

{% if cookiecutter.use_auth0 | bool %}
from src.authentication import AuthUser, get_user
from src.authentication import Permissions
{% endif -%}

test_router = APIRouter(tags=["Automated Testing Routes"])


@test_router.get("/openroute/")
async def route_unrestricted():
    return {"success": True}


{% if cookiecutter.use_auth0 | bool -%}
@test_router.get("/authenticated/")
async def route_requiring_auth(user: Annotated[AuthUser, Security(get_user(), scopes=[])]):
    return {"success": True}


@test_router.get("/permission/")
async def route_requiring_permission(
        user: Annotated[AuthUser, Security(get_user(), scopes=[Permissions.ADMIN])]
):
    return {"success": True}
{% endif -%}

