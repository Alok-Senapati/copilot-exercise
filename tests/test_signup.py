"""
Tests for POST /activities/{activity_name}/signup endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignup:
    """Tests for signing up a student to an activity"""

    def test_valid_signup_adds_participant(self, client, fresh_activities):
        """
        Arrange: Set up a valid email and activity
        Act: POST to signup endpoint
        Assert: Participant is added and status is 200
        """
        # Arrange
        activity_name = "Gym Class"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email in fresh_activities["Gym Class"]["participants"]
        assert "Signed up" in response.json()["message"]

    def test_signup_returns_success_message(self, client, fresh_activities):
        """
        Arrange: Prepare valid signup data
        Act: Sign up a student
        Assert: Response contains expected success message
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_returns_400(self, client, fresh_activities):
        """
        Arrange: Student is already signed up for an activity
        Act: Attempt to sign up again
        Assert: Returns 400 with 'already signed up' message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Arrange: Use an activity name that doesn't exist
        Act: POST to signup endpoint with invalid activity
        Assert: Returns 404 Activity not found
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_invalid_email_format_returns_400(self, client, fresh_activities):
        """
        Arrange: Use invalid email formats
        Act: POST signup with invalid emails
        Assert: Returns 400 with invalid email format message
        """
        # Arrange
        activity_name = "Gym Class"
        invalid_emails = ["notanemail", "missing@domain", "@nodomain.com", ""]
        
        # Act & Assert
        for invalid_email in invalid_emails:
            response = client.post(f"/activities/{activity_name}/signup?email={invalid_email}")
            assert response.status_code == 400
            assert "Invalid email format" in response.json()["detail"]

    def test_signup_at_capacity_returns_400(self, client, fresh_activities):
        """
        Arrange: Fill an activity to max capacity
        Act: Attempt to sign up when at capacity
        Assert: Returns 400 with 'at capacity' message
        """
        # Arrange - Fill Basketball Team to capacity (max 15)
        activity_name = "Basketball Team"
        for i in range(15):
            fresh_activities["Basketball Team"]["participants"].append(f"student{i}@mergington.edu")
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email=newstudent@mergington.edu")
        
        # Assert
        assert response.status_code == 400
        assert "at capacity" in response.json()["detail"]

    def test_signup_increases_participant_count(self, client, fresh_activities):
        """
        Arrange: Get initial participant count
        Act: Sign up a new student
        Assert: Participant count increases by 1
        """
        # Arrange
        activity_name = "Tennis Club"
        initial_count = len(fresh_activities["Tennis Club"]["participants"])
        email = "newplayer@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        new_count = len(fresh_activities["Tennis Club"]["participants"])
        
        # Assert
        assert response.status_code == 200
        assert new_count == initial_count + 1

    def test_signup_with_valid_mergington_email(self, client, fresh_activities):
        """
        Arrange: Use a standard Mergington High School email
        Act: Sign up with valid email format
        Assert: Signup succeeds
        """
        # Arrange
        activity_name = "Drama Club"
        email = "john.doe@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email in fresh_activities["Drama Club"]["participants"]
