"""
Tests for POST /activities/{activity_name}/unregister endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestUnregister:
    """Tests for unregistering a student from an activity"""

    def test_valid_unregister_removes_participant(self, client, fresh_activities):
        """
        Arrange: Student is registered for an activity
        Act: POST to unregister endpoint
        Assert: Participant is removed and status is 200
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert email not in fresh_activities["Chess Club"]["participants"]

    def test_unregister_returns_success_message(self, client, fresh_activities):
        """
        Arrange: Prepare valid unregister data
        Act: Unregister a student
        Assert: Response contains expected success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]

    def test_unregister_student_not_found_returns_404(self, client, fresh_activities):
        """
        Arrange: Student is not registered for the activity
        Act: Attempt to unregister non-participant
        Assert: Returns 404 with 'Student not found' message
        """
        # Arrange
        activity_name = "Gym Class"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Student not found" in response.json()["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client, fresh_activities):
        """
        Arrange: Activity doesn't exist
        Act: POST to unregister from non-existent activity
        Assert: Returns 404 Activity not found
        """
        # Arrange
        activity_name = "Fake Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_decreases_participant_count(self, client, fresh_activities):
        """
        Arrange: Get initial participant count
        Act: Unregister a student
        Assert: Participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(fresh_activities["Chess Club"]["participants"])
        
        # Act
        response = client.post(f"/activities/{activity_name}/unregister?email={email}")
        new_count = len(fresh_activities["Chess Club"]["participants"])
        
        # Assert
        assert response.status_code == 200
        assert new_count == initial_count - 1

    def test_cannot_unregister_twice(self, client, fresh_activities):
        """
        Arrange: Unregister a student once
        Act: Attempt to unregister the same student again
        Assert: Second unregister returns 404
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act - First unregister
        response1 = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Act - Second unregister
        response2 = client.post(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_unregister_frees_up_capacity(self, client, fresh_activities):
        """
        Arrange: Activity is at capacity, then unregister someone
        Act: Sign up new student after unregistering
        Assert: New signup succeeds because capacity was freed
        """
        # Arrange - Fill activity to capacity
        activity_name = "Art Studio"
        fresh_activities["Art Studio"]["participants"] = [f"student{j}@mergington.edu" for j in range(18)]
        
        email_to_remove = "student0@mergington.edu"
        new_email = "newstudent@mergington.edu"
        
        # Act - Unregister to free space
        response_unregister = client.post(f"/activities/{activity_name}/unregister?email={email_to_remove}")
        
        # Act - Try to sign up new student
        response_signup = client.post(f"/activities/{activity_name}/signup?email={new_email}")
        
        # Assert
        assert response_unregister.status_code == 200
        assert response_signup.status_code == 200
        assert new_email in fresh_activities["Art Studio"]["participants"]
