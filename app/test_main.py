import pytest, httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_word_counter():
    response = client.get("/word-count")
    assert response.status_code == 200
    assert response.json() == []

def test_post_word_counter():
    data = {"keyword": "example", "url": "https://example.com/"}
    response = client.post("/word-count", json=data)
    assert response.status_code == 200
    assert response.json()["keyword"] == "example"
    assert response.json()["url"] == "https://example.com/"
    assert response.json()["count"] > 0

def test_post_word_counter_none_found():
    data = {"keyword": "technology", "url": "https://example.com/"}
    response = client.post("/word-count", json=data)
    assert response.status_code == 200
    assert response.json()["keyword"] == "technology"
    assert response.json()["url"] == "https://example.com/"
    assert response.json()["count"] == 0

def test_post_word_counter_invalid_url():
    data = {"keyword": "example", "url": "invalid_url"}
    response = client.post("/word-count", json=data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Input should be a valid URL, relative URL without a base"

def test_post_word_counter_request_exception():
    data = {"keyword": "example", "url": "https://does-not-exist.com"}
    response = client.post("/word-count", json=data)
    assert response.status_code == 422
    assert response.json()['detail'] == f"Failed to fetch webpage content from {data['url']}/"