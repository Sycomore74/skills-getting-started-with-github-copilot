import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_participant_from_activity():
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    original_participants = list(activities[activity_name]["participants"])

    response = client.delete(
        f"/activities/{activity_name}/participants/{participant_email}"
    )

    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {participant_email} from {activity_name}"

    activities[activity_name]["participants"] = original_participants
