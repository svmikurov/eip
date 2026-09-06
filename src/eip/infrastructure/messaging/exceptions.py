"""Messaging exceptions."""


class QueueCircuitOpen(Exception):
    """Raised when the queue rejects new messages to prevent overload.

    This is a controlled degradation mechanism, not a system failure.
    The caller should implement backoff or fallback logic.
    """
