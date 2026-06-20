from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

class MatchingLayer(str, Enum):
    """Layer of the fuzzy matching system that identified the command."""
    EXACT = "exact"
    PHONETIC = "phonetic"
    LEVENSHTEIN = "levenshtein"
    SYNONYM = "synonym"
    ALIAS = "alias"
    FALLBACK = "fallback"

class DangerLevel(str, Enum):
    """Level of potential danger associated with a command."""
    LOW = "low"
    HIGH = "high"

class TriggerSource(str, Enum):
    """How the command is triggered."""
    VOICE = "voice"
    KEYBOARD = "keyboard"
    SCHEDULED = "scheduled"
    REST_API = "rest_api"
    PLUGIN = "plugin"

class MessageRole(str, Enum):
    """Role of a message in a conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class Command:
    """
    Attributes:
        id: Unique identifier for the command
        raw_text: The original text of the command as recognized
        normalized_text: The normalized text used for matching
        matching_layer: The layer of the fuzzy matching system that identified the command
        timestamp: When the command was issued
        context: the context snapshot at time of command
        is_dangerous: Whether the command is potentially dangerous
        requires_confirmation: Whether the command requires user confirmation before execution"""
    id: UUID = field(default_factory=uuid4)
    raw_text: str = ""
    normalized_text: str = ""
    confidence: float = 0.0
    matched_layer: Optional[MatchingLayer] = None
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[Dict[str, Any]] = None
    is_dangerous: bool = False
    requires_confirmation: bool = False
    shortcut_name: Optional[str] = None

@dataclass
class Alias:
    """Attributes:
        voice_phrase: the phrase the users says
        shortcut_name: the shortcut to run
        danger_level: whether this command is dangerous
        is_safe: whether this alias is safe for sandbox mode
        variables: optional variable placeholders
        context_overrides: app specific mappings
        """
    voice_phrase: str
    shortcut_name: str
    danger_level: DangerLevel = DangerLevel.LOW
    is_safe: bool = True
    variables: Optional[Dict[str, Any]] = None
    context_overrides: Optional[Dict[str, Any]] = None

@dataclass
class ContextSnapshot:
    """
    Attributes:
        active_app: the frontmost application name
        active_window_title: the frontmost window title
        selected_text: any text currently selected by the user
        files_touched: files accessed/modified in this session
        current_session_duration: how long the current session has been active
        last_build_status: last build status
        calendar_events: upcoming calendar events
        is_idle: whether the system is idle
        idle_duration: how long the system has been idle
        keyboard_activity: recent keyboard activity level
        """
    active_app: str = ""
    active_window_title: str = ""
    selected_text: Optional[str] = None
    files_touched: List[str] = field(default_factory=list)
    current_session_duration: float = 0.0
    last_build_status: Optional[str] = None
    calendar_events: List[Dict[str, Any]] = field(default_factory=list)
    is_idle: bool = False
    idle_duration: Optional[float] = None
    keyboard_activity: str = "idle"

@dataclass
class MemoryRecord:
    """ Attributes:
        command: the raw command text
        shortcut_executed: the shortcut that was run
        timestamp: when the command was executed
        execution_duration: how long execution took
        sucess: whether execution succeeded
        context: the context snapshot at time of execution
        source: how the command was triggered
        output: any output from the shortcut
        error: any error message
        """
    command: str
    shortcut_executed: str
    timestamp: datetime = field(default_factory=datetime.now)
    execution_duration: float = 0.0
    success: bool = False
    context: Optional[ContextSnapshot] = None
    source: TriggerSource = TriggerSource.VOICE
    output: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ConversationMessage:
    """Attributes:
        role: the role of the message sender
        content: the message content
        timestamp: when the message was sent
        """
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now
    )

@dataclass
class Conversation:
    """Attributes:
        id: Unique identifier for the conversation
        message: list of message in the conversation
        context: the context snapshot at conversation
        is_active: whether the conversation is current active
        llm_model: which llm model is being used
        started_at: when the conversation started
        last_active: when the last message was sent
        """
    id: UUID = field(default_factory=uuid4)
    messages: List[ConversationMessage] = field(default_factory=list)
    context: Optional[ContextSnapshot] = None
    is_active: bool = False
    llm_model: str = "llama3"
    started_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

        
    