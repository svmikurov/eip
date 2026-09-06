"""Message layer.

Base messaging component — Message (EIP, p. 98).
"""

from dataclasses import dataclass


@dataclass
class PredictionCommand:
    """Command message requesting a prediction.

    Sender sets correlation_id and reply_to to receive the response.
    """

    request_id: str
    correlation_id: str | None = None
    reply_to: str | None = None
    body: str = ""


@dataclass
class PredictionDocument:
    """Response message containing the prediction result.

    Carries the same correlation_id as the original request.
    """

    request_id: str
    correlation_id: str
    body: str = ""
