"""Tests for authentication API endpoints."""
import pytest


def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email."""
    # First registration
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201

    # Duplicate registration
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400


def test_login_success(client, test_user_data):
    """Test successful login."""
    # Register first
    client.post("/api/v1/auth/register", json=test_user_data)

    # Login
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password."""
    # Register first
    client.post("/api/v1/auth/register", json=test_user_data)

    # Login with wrong password
    login_data = {
        "username": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401


def test_logout():
    """Test logout endpoint."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "成功登出"


def test_get_current_user(client, auth_headers):
    """Test getting current user profile."""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "email" in data
    assert "id" in data
