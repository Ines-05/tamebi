import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Patch Supabase client before importing anything from the app
with patch("app.database.create_client") as _mock:
    _mock.return_value = MagicMock()
    from app.main import app

client = TestClient(app)


# ── Helpers ────────────────────────────────────────────────────────────────────

def mock_insert_ok(alias: str):
    mock = MagicMock()
    mock.table.return_value.insert.return_value.execute.return_value = MagicMock(
        data=[{"alias": alias, "created_at": "2024-01-01T00:00:00+00:00"}]
    )
    return mock


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_auto_generate():
    with patch("app.routes.shorten.alias_exists", return_value=False), \
         patch("app.routes.shorten.supabase", mock_insert_ok("abc123")):
        res = client.post("/shorten", json={"original_url": "https://example.com"})
        assert res.status_code == 201
        body = res.json()
        assert "short_url" in body
        assert body["is_custom"] is False


def test_custom_alias_success():
    with patch("app.routes.shorten.alias_exists", return_value=False), \
         patch("app.routes.shorten.supabase", mock_insert_ok("mylink")):
        res = client.post("/shorten", json={
            "original_url": "https://example.com",
            "custom_alias": "mylink"
        })
        assert res.status_code == 201
        assert res.json()["alias"] == "mylink"
        assert res.json()["is_custom"] is True


def test_custom_alias_taken():
    with patch("app.routes.shorten.alias_exists", return_value=True):
        res = client.post("/shorten", json={
            "original_url": "https://example.com",
            "custom_alias": "taken"
        })
        assert res.status_code == 409


def test_invalid_alias_format():
    res = client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_alias": "bad alias!"   # spaces and ! not allowed
    })
    assert res.status_code == 422


def test_alias_too_short():
    res = client.post("/shorten", json={
        "original_url": "https://example.com",
        "custom_alias": "ab"            # under 3 chars
    })
    assert res.status_code == 422


def test_invalid_url():
    res = client.post("/shorten", json={"original_url": "not-a-url"})
    assert res.status_code == 422


def test_expiry_out_of_range():
    res = client.post("/shorten", json={
        "original_url": "https://example.com",
        "expires_in_days": 400
    })
    assert res.status_code == 422


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}