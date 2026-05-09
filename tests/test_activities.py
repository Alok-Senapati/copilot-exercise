"""
Tests for GET /activities endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities"""

    def test_get_all_activities_returns_success(self, client, fresh_activities):
        """
        Arrange: Fresh activities fixture is used
        Act: Make GET request to /activities
        Assert: Status is 200 and response contains activities
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_returns_all_nine_activities(self, client, fresh_activities):
        """
        Arrange: Activities database is loaded
        Act: Fetch all activities
        Assert: Response contains exactly 9 activities
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert len(activities_data) == 9
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data

    def test_activity_has_required_fields(self, client, fresh_activities):
        """
        Arrange: Fetch activities endpoint
        Act: Get activities and check first activity structure
        Assert: Activity object has all required fields
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_activity_participants_are_emails(self, client, fresh_activities):
        """
        Arrange: Fetch activities with participants
        Act: Get an activity with participants
        Assert: Participants list contains email strings
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        chess_participants = activities_data["Chess Club"]["participants"]
        
        # Assert
        assert len(chess_participants) > 0
        assert all("@" in participant for participant in chess_participants)

    def test_participant_count_matches_list_length(self, client, fresh_activities):
        """
        Arrange: Get activities
        Act: Verify consistency of participant data
        Assert: Participant count makes sense with max_participants
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_data in activities_data.items():
            participant_count = len(activity_data["participants"])
            max_allowed = activity_data["max_participants"]
            assert participant_count <= max_allowed
