from typing import Tuple

from .DigitalAssistantMediaRouter_pb2_grpc import DigitalAssistantMediaRouterStub
from .DigitalAssistantMediaRouter_pb2 import (
    DigitalAssistantMediaRouterRequest,
    DigitalAssistantMediaRouterResponse,
)
from .abstract_client import AbstractClient


ResourceId = str
Interpretation = str

class MediaRouterClient(AbstractClient):
    def __init__(self, address):
        super().__init__(address)
        self._stub = DigitalAssistantMediaRouterStub(self._channel)

    def __call__(
        self, resource_id: str, prompt: str, request_id: str = ""
    ) -> Tuple[ResourceId, Interpretation]:
        request = DigitalAssistantMediaRouterRequest(
            RequestId=request_id,
            ResourceId=resource_id,
            Prompt=prompt,
        )
        response: DigitalAssistantMediaRouterResponse = self._stub.Interpret(request)
        return response.ResourceId, response.Interpretation
