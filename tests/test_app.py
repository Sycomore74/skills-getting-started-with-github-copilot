import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    original_activities = copy.deepcopy(activities)

    with TestClient(app) as test_client:
        yield test_client

    activities.clear()
    activities.update(original_activities)


def test_get_activities_returns_activity_data(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity_name in response.json()


def test_unregister_participant_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{participant_email}"
    )

    # Assert
    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]
    assert response.json() == {
        "message": f"Unregistered {participant_email} from {activity_name}"
    }
