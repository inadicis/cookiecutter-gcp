import base64
import dataclasses
import json
from typing import Callable

import pytest
import datetime

from src import routes
from src.config.env_settings import EnvSettings


@pytest.fixture()
def body_wrapper() -> Callable[[dict, dict], dict]:
    def _wrap_body(body: dict, attributes: dict | None = None) -> dict:
        """ Simulates a pubsub message """
        encoded_body = str(base64.b64encode(json.dumps(body).encode("utf-8")))[2:-1]
        return {
            "message": {
                "data": encoded_body,
                "attributes": attributes,
                "message_id": "some_unique_id",
                "publish_time": datetime.datetime.now().isoformat(),
            },
            "subscription": "my_gcp_subscription"
        }

    yield _wrap_body


@pytest.fixture()
def patch_external_requests(monkeypatch):
    # mock the publish back to queue
    @dataclasses.dataclass
    class FakeFuture:
        response_message: dict
        settings: EnvSettings

        def result(self, *args, **kwargs):
            return self.response_message

    monkeypatch.setattr(
        routes,
        "publish_response",
        FakeFuture
    )
    # not testing the actual function, just view level logic:
    monkeypatch.setattr(
        routes,
        "business_logic",
        lambda *args, **kwargs: "mocked"
    )


@pytest.mark.parametrize(
    ["body", "attributes", "expected_status", "expected_success", "test_description"],
    [
        [
            {
                "original": "hello this is an original content",
            },
            {},
            200,
            True,
            "Typical request service, should work"
        ],
        # [
        #     {
        #         "original": "hello this is an original content",
        #         "reduce_by_percentage": 10,
        #     },
        #     {
        #         "destination": pubsub.Destinations.SUMMARIZER,
        #         "origin": "my_service",
        #         "type": pubsub.PubsubMessageTypes.RESPONSE
        #     },
        #     422,
        #     False,
        #     "wrong attributes.type: is response instead of request. this should never happen - "
        #     "the subscription filter should avoid this"
        # ],
        [
            {"otherparam": 4},
            {},
            200,
            False,
            "Should not work: some required options are missing (`original`)"
        ],
    ]
)
@pytest.mark.asyncio
async def test_pubsub_route(
        client,
        monkeypatch,
        body,
        attributes,
        expected_success,
        body_wrapper,
        test_description,
        patch_external_requests,
        expected_status
):
    pubsub_body = body_wrapper(body, attributes)
    response = client.post(url="/pubsub", json=pubsub_body)
    assert response.status_code == expected_status
    if expected_status < 300:
        assert response.json()["success"] == expected_success
    # N.B We patched the response to contain the result body. The actual responses
    #  will only contain the publish message id (future.result())
