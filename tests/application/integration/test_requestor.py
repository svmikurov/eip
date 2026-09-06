"""Requestor tests."""

from unittest.mock import Mock

import pytest

from eip.application.gateways import Requestor
from eip.application.messages import PredictionDocument
from eip.application.protocols import ConsumerProto, ProducerProto

REQUEST_ID = "123ABC"
CONTENT = "Text"
RESULT = "Result"


@pytest.fixture
def mock_producer() -> Mock:
    """Provide producer mock."""
    return Mock(spec=ProducerProto)


@pytest.fixture
def mock_consumer() -> Mock:
    """Provide consumer mock."""
    mock = Mock(spec=ConsumerProto)
    mock.receive.return_value = PredictionDocument(
        request_id=REQUEST_ID,
        correlation_id=REQUEST_ID,
        body=RESULT,
    )
    return mock


@pytest.fixture
def mock_invalid_producer() -> Mock:
    """Provide invalid producer mock."""
    return Mock(spec=ProducerProto)


@pytest.fixture
def requestor(
    mock_producer: ProducerProto,
    mock_consumer: ConsumerProto,
    mock_invalid_producer: ProducerProto,
) -> Requestor:
    """Provide requestor."""
    return Requestor(
        mock_producer,
        mock_consumer,
        mock_invalid_producer,
    )


async def test_request_returns_result(
    requestor: Requestor,
) -> None:
    # Act
    result = await requestor.request(REQUEST_ID, CONTENT)

    # Assert
    assert result == RESULT
