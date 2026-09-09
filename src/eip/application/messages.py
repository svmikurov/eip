"""Messages (EIP, p. 98)."""

from dataclasses import dataclass


@dataclass
class Command:
    """Simple Command Message."""

    request_id: str
    body: str = ''


@dataclass
class PredictionCommand:
    """Command message requesting a prediction."""

    request_id: str
    correlation_id: str | None = None
    reply_to: str | None = None
    body: str = ''


@dataclass
class PredictionDocument:
    """Response message containing the prediction result."""

    request_id: str
    correlation_id: str
    body: str = ''
