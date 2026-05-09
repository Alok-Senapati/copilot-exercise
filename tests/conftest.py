"""
Pytest configuration and shared fixtures for the test suite.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Arrange: Provide a TestClient connected to the FastAPI app.
    This fixture is used by all tests to make HTTP requests.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities(client):
    """
    Arrange: Reset activities to a known clean state before each test.
    This ensures tests don't interfere with each other.
    """
    # Clear existing participants and reset to initial state
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu"]
    activities["Gym Class"]["participants"] = []
    activities["Basketball Team"]["participants"] = []
    activities["Tennis Club"]["participants"] = []
    activities["Drama Club"]["participants"] = []
    activities["Art Studio"]["participants"] = []
    activities["Debate Team"]["participants"] = []
    activities["Science Club"]["participants"] = []
    return activities
