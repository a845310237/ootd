"""Tests for wardrobe API endpoints."""
import pytest
import json


def test_create_clothing(client, auth_headers):
    """Test creating a clothing item."""
    clothing_data = {
        "name": "Test T-Shirt",
        "category": "上衣",
        "color": json.dumps(["白色", "黑色"]),
        "style": json.dumps(["休闲"]),
        "season": json.dumps(["夏"]),
        "image_url": "https://example.com/shirt.jpg"
    }

    response = client.post("/api/v1/wardrobe", json=clothing_data, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == clothing_data["name"]
    assert data["category"] == clothing_data["category"]
    assert "id" in data


def test_get_wardrobe(client, auth_headers):
    """Test getting user's wardrobe."""
    # Create some clothing items first
    for i in range(3):
        clothing_data = {
            "name": f"Test Item {i}",
            "category": "上衣",
            "image_url": "https://example.com/shirt.jpg"
        }
        client.post("/api/v1/wardrobe", json=clothing_data, headers=auth_headers)

    # Get wardrobe
    response = client.get("/api/v1/wardrobe", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3


def test_get_wardrobe_with_filter(client, auth_headers):
    """Test filtering wardrobe by category."""
    # Create items in different categories
    client.post("/api/v1/wardrobe", json={
        "name": "T-Shirt",
        "category": "上衣",
        "image_url": "https://example.com/shirt.jpg"
    }, headers=auth_headers)

    client.post("/api/v1/wardrobe", json={
        "name": "Jeans",
        "category": "裤子",
        "image_url": "https://example.com/jeans.jpg"
    }, headers=auth_headers)

    # Filter by category
    response = client.get("/api/v1/wardrobe?category=上衣", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "上衣"


def test_delete_clothing(client, auth_headers):
    """Test deleting a clothing item."""
    # Create item
    clothing_data = {
        "name": "Test Item",
        "category": "上衣",
        "image_url": "https://example.com/shirt.jpg"
    }
    response = client.post("/api/v1/wardrobe", json=clothing_data, headers=auth_headers)
    clothing_id = response.json()["id"]

    # Delete item
    response = client.delete(f"/api/v1/wardrobe/{clothing_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get("/api/v1/wardrobe", headers=auth_headers)
    assert len(response.json()) == 0
