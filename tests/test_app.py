from fastapi.testclient import TestClient
from src.app import app
from urllib.parse import quote

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate():
    act = "Basketball Team"
    email = "tester@mergington.edu"
    signup_path = f"/activities/{quote(act)}/signup?email={quote(email)}"

    # First signup should succeed
    r1 = client.post(signup_path)
    assert r1.status_code == 200
    body = r1.json()
    assert email in body.get("activity", {}).get("participants", [])

    # Duplicate signup should be rejected
    r2 = client.post(signup_path)
    assert r2.status_code == 400


def test_unregister_participant():
    act = "Basketball Team"
    email = "tester@mergington.edu"
    delete_path = f"/activities/{quote(act)}/participants?email={quote(email)}"

    # Unregister the participant
    r = client.delete(delete_path)
    assert r.status_code == 200

    # Verify participant no longer listed
    data = client.get("/activities").json()
    assert email not in data[act]["participants"]
