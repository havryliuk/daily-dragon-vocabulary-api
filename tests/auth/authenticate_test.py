import os
import pytest
from unittest import mock
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from daily_dragon.auth.authenticate import authenticate, get_password, get_password_from_secrets


@pytest.fixture
def mock_boto3_client():
    with mock.patch("boto3.client") as mock_client:
        yield mock_client

@pytest.fixture
def credentials():
    return HTTPBasicCredentials(username="havryliuk", password="test_pw")

def test_get_password_from_secrets_success(mock_boto3_client):
    stub_secret = "secret_pw"
    mock_secrets_manager = mock.Mock()
    mock_secrets_manager.get_secret_value.return_value = {"SecretString": stub_secret}
    mock_boto3_client.return_value = mock_secrets_manager

    with mock.patch.dict(os.environ, {"AWS_REGION": "us-custom", "PASSWORD_SECRET_ID": "test_secret"}):
        result = get_password_from_secrets()
    assert result == stub_secret
    mock_boto3_client.assert_called_once_with("secretsmanager", region_name="us-custom")
    mock_secrets_manager.get_secret_value.assert_called_once_with(SecretId="test_secret")

def test_get_password_from_secrets_client_error(mock_boto3_client):
    mock_secrets_manager = mock.Mock()
    mock_secrets_manager.get_secret_value.side_effect = Exception("Some exception")
    mock_boto3_client.return_value = mock_secrets_manager

    with pytest.raises(Exception):
        get_password_from_secrets()

def test_get_password_uses_env(monkeypatch):
    monkeypatch.setenv("PASSWORD", "envpw")
    res = get_password()
    assert res == "envpw"

def test_get_password_uses_secrets(monkeypatch, mock_boto3_client):
    monkeypatch.delenv("PASSWORD", raising=False)
    stub_secret = '{"SecretString": "itsasecret"}'
    mock_secrets_manager = mock.Mock()
    mock_secrets_manager.get_secret_value.return_value = {"SecretString": stub_secret}
    mock_boto3_client.return_value = mock_secrets_manager

    out = get_password()
    assert out == "itsasecret"

def test_authenticate_success(monkeypatch):
    monkeypatch.setenv("PASSWORD", "pw")
    creds = HTTPBasicCredentials(username="havryliuk", password="pw")

    result = authenticate(creds)
    assert result == "havryliuk"

def test_authenticate_incorrect_username(monkeypatch):
    monkeypatch.setenv("PASSWORD", "pw")
    creds = HTTPBasicCredentials(username="notuser", password="pw")

    with pytest.raises(HTTPException) as exc:
        authenticate(creds)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_authenticate_incorrect_password(monkeypatch):
    monkeypatch.setenv("PASSWORD", "pw")
    creds = HTTPBasicCredentials(username="havryliuk", password="wrong")

    with pytest.raises(HTTPException) as exc:
        authenticate(creds)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
