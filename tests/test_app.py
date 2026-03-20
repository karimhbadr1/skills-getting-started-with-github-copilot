import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

BASE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    for key, value in BASE_ACTIVITIES.items():
        activities[key] = {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": list(value["participants"]),
        }


def test_get_activities_returns_initial_data():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant():
    signup_response = client.post("/activities/Chess%20Club/signup?email=alex@mergington.edu")
    assert signup_response.status_code == 200
    assert "Signed up alex@mergington.edu for Chess Club" in signup_response.json()["message"]

    activities_response = client.get("/activities").json()
    assert "alex@mergington.edu" in activities_response["Chess Club"]["participants"]


def test_signup_duplicate_participant_returns_400():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant already registered"


def test_remove_participant():
    delete_response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")
    assert delete_response.status_code == 200

    activities_response = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities_response["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_404():
    delete_response = client.delete("/activities/Chess%20Club/participants?email=notfound@mergington.edu")
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Participant not found"


def test_remove_activity_not_found_returns_404():
    delete_response = client.delete("/activities/Nope/participants?email=doe@mergington.edu")
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Activity not found"
