import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from daily_dragon.auth.authenticate import authenticate
from daily_dragon.daily_dragon_app import app
from daily_dragon.service.vocabulary_service import VocabularyService


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def test_client(mock_service):
    app.dependency_overrides = dict()
    app.dependency_overrides[VocabularyService] = lambda: mock_service
    app.dependency_overrides[authenticate] = lambda: "havryliuk"

    client = TestClient(app)
    yield client

    app.dependency_overrides = {}
