from typing import Any

from .commons_pb2 import OuterContextItem
from .DigitalAssistantChatManager_pb2_grpc import DigitalAssistantChatManagerStub
from .DigitalAssistantChatManager_pb2 import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
)
from .abstract_client import AbstractClient


class ChatManagerClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantChatManagerStub(self._channel)

    def __call__(self, text: str, outer_context: dict, request_id: str, resource_id: str) -> str:
        request = DigitalAssistantChatManagerRequest(
            Text=text,
            OuterContext=OuterContextItem(
                Sex=outer_context["Sex"],
                Age=outer_context["Age"],
                UserId=outer_context["UserId"],
                SessionId=outer_context["SessionId"],
                ClientId=outer_context["ClientId"],
                TrackId=outer_context["TrackId"],
            ),
            RequestId=request_id,
            ResourceId=resource_id,
        )
        response: DigitalAssistantChatManagerResponse = self._stub.GetChatResponse(
            request
        )
        replica: dict[str, Any] = {
            "Text": response.Text,
            "ResourceId": response.ResourceId,
            "State": response.State,
            "Action": response.Action,
        }
        return replica
