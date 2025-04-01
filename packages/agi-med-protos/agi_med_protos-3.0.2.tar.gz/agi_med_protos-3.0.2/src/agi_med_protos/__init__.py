__version__ = "3.0.2"

# common
from .commons_pb2 import (
    InnerContextItem,
    ChatItem,
    ReplicaItem,
    OuterContextItem,
)

# Text
from .text_client import TextClient
from .DigitalAssistantText_pb2 import (
    DigitalAssistantTextRequest,
    DigitalAssistantTextResponse,
)
from .DigitalAssistantText_pb2_grpc import (
    DigitalAssistantText,
    DigitalAssistantTextServicer,
    DigitalAssistantTextStub,
    add_DigitalAssistantTextServicer_to_server,
)
# add_DigitalAssistantTextServicer_to_server

# Critic
from .critic_client import CriticClient
from .DigitalAssistantCritic_pb2 import (
    DigitalAssistantCriticRequest,
    DigitalAssistantCriticResponse,
)
from .DigitalAssistantCritic_pb2_grpc import (
    DigitalAssistantCritic,
    DigitalAssistantCriticServicer,
    DigitalAssistantCriticStub,
    add_DigitalAssistantCriticServicer_to_server
)

# ChatManager
from .chat_manager_client import ChatManagerClient
from .DigitalAssistantChatManager_pb2 import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
)
from .DigitalAssistantChatManager_pb2_grpc import (
    DigitalAssistantChatManager,
    DigitalAssistantChatManagerServicer,
    DigitalAssistantChatManagerStub,
    add_DigitalAssistantChatManagerServicer_to_server,
)

# OCR
from .ocr_client import OCRClient
from .DigitalAssistantOCR_pb2 import (
    DocType,
    DigitalAssistantOCRRequest,
    DigitalAssistantOCRResponse,
)
from .DigitalAssistantOCR_pb2_grpc import (
    DigitalAssistantOCR,
    DigitalAssistantOCRServicer,
    DigitalAssistantOCRStub,
    add_DigitalAssistantOCRServicer_to_server,
)

# MediaRouter
from .media_router_client import MediaRouterClient
from .DigitalAssistantMediaRouter_pb2 import (
    DigitalAssistantMediaRouterRequest,
    DigitalAssistantMediaRouterResponse,
)
from .DigitalAssistantMediaRouter_pb2_grpc import (
    DigitalAssistantMediaRouter,
    DigitalAssistantMediaRouterServicer,
    DigitalAssistantMediaRouterStub,
    add_DigitalAssistantMediaRouterServicer_to_server,
)
