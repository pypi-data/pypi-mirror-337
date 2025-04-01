__version__ = "3.0.0"

# common
from .commons_pb2 import (
    InnerContextItem,
    ChatItem,
    ReplicaItem,
    OuterContextItem,
)

# Text
from .text_client import TextClient
from .DigitalAssistantText_pb2_grpc import (
    DigitalAssistantText,
    DigitalAssistantTextServicer,
    DigitalAssistantTextStub,
)

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
)
