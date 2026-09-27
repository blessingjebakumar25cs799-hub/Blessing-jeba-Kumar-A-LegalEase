from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.json()["service"]
        == "LegalEase"
    )


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_generate_with_mock(monkeypatch):

    class FakeGenerator:

        def __init__(self, _settings):
            pass

        def generate_document(self, **kwargs):

            assert (
                kwargs["document_type"]
                == "Non-Disclosure Agreement"
            )

            return (
                "NON-DISCLOSURE AGREEMENT\n\n"
                "1. CONFIDENTIALITY\n"
                "The parties agree."
            )

    monkeypatch.setattr(
        "backend.routes.GeminiDocumentGenerator",
        FakeGenerator,
    )

    response = client.post(
        "/generate",
        json={
            "document_type":
                "Non-Disclosure Agreement",

            "parties":
                "Jane Doe, TechNova Inc.",

            "terms":
                "Confidentiality must be maintained",

            "effective_date":
                "2026-09-25",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["document_type"]
        == "Non-Disclosure Agreement"
    )

    assert (
        "CONFIDENTIALITY"
        in body["content"]
    )


def test_generate_validation():

    response = client.post(
        "/generate",
        json={
            "document_type": "",
            "parties": "A, B",
            "terms": "Confidentiality",
            "effective_date": "2026-09-25",
        },
    )

    assert response.status_code == 422