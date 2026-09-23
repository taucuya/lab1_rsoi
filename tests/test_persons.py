import pytest
from fastapi.testclient import TestClient

PERSON = {
    "name": "John Doe",
    "address": "Baker Street 221B",
    "work": "Detective",
    "age": 31,
}


def test_create_person_returns_201_and_location(client: TestClient):
    response = client.post("/api/v1/persons", json=PERSON)
    assert response.status_code == 201
    assert response.text == ""
    location = response.headers.get("Location")
    assert location is not None
    assert location.startswith("/api/v1/persons/")
    assert int(location.rsplit("/", 1)[-1]) > 0


def test_get_person_by_id(client: TestClient):
    created = client.post("/api/v1/persons", json=PERSON)
    location = created.headers["Location"]
    person_id = int(location.rsplit("/", 1)[-1])

    response = client.get(f"/api/v1/persons/{person_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    body = response.json()
    assert body["id"] == person_id
    assert body["name"] == PERSON["name"]
    assert body["address"] == PERSON["address"]
    assert body["work"] == PERSON["work"]
    assert body["age"] == PERSON["age"]


def test_get_all_persons_contains_created_person(client: TestClient):
    client.post("/api/v1/persons", json=PERSON)

    response = client.get("/api/v1/persons")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    matches = [p for p in body if p["name"] == PERSON["name"] and p["address"] == PERSON["address"]]
    assert len(matches) >= 1


def test_patch_person_updates_only_provided_fields(client: TestClient):
    created = client.post("/api/v1/persons", json=PERSON)
    location = created.headers["Location"]
    person_id = int(location.rsplit("/", 1)[-1])

    patch = {"name": "Jane Smith", "address": "Elm Street 42"}
    response = client.patch(f"/api/v1/persons/{person_id}", json=patch)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == person_id
    assert body["name"] == "Jane Smith"
    assert body["address"] == "Elm Street 42"
    assert body["work"] == PERSON["work"]
    assert body["age"] == PERSON["age"]


def test_delete_person_returns_204_and_person_disappears(client: TestClient):
    created = client.post("/api/v1/persons", json=PERSON)
    location = created.headers["Location"]
    person_id = int(location.rsplit("/", 1)[-1])

    response = client.delete(f"/api/v1/persons/{person_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/persons/{person_id}")
    assert response.status_code == 404
