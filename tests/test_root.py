"""
Tests for GET / endpoint.
Uses AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRoot:
    """Tests for root endpoint redirect"""

    def test_root_redirects_to_static_index(self, client):
        """
        Arrange: Request the root endpoint
        Act: Make GET request to /
        Assert: Returns redirect status and correct location
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]

    def test_root_with_follow_redirects_returns_html(self, client):
        """
        Arrange: Request root with redirect following
        Act: Make GET request to / with follow_redirects=True
        Assert: Returns 200 and HTML content
        """
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
