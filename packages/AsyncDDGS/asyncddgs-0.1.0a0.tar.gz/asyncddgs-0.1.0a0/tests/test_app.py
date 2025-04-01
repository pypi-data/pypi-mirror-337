import pytest
import requests
import time

BASE_URL = "http://localhost:8080"

@pytest.fixture
def rate_limit_delay():
    """Fixture to enforce a delay after each test to respect DuckDuckGo's rate limits."""
    yield
    time.sleep(25)  # 25-second delay to prevent rate limit issues

# Text Search Tests
def test_text_search_success(rate_limit_delay):
    """Test a successful text search with default parameters."""
    payload = {"keywords": "python programming"}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    for result in data["results"]:
        assert "title" in result
        assert "href" in result
        assert "body" in result

def test_text_search_max_results(rate_limit_delay):
    """Test text search respects the max_results parameter."""
    payload = {"keywords": "python programming", "max_results": 3}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 3

def test_text_search_invalid_safesearch(rate_limit_delay):
    """Test error handling for invalid safesearch value."""
    payload = {"keywords": "python programming", "safesearch": "invalid"}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_text_search_empty_keywords(rate_limit_delay):
    """Test error handling for empty keywords."""
    payload = {"keywords": ""}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_image_search_success(rate_limit_delay):
    payload = {"keywords": "nature"}
    response = requests.post(f"{BASE_URL}/images", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    for result in data["results"]:
        assert "title" in result
        assert "image" in result
        assert "thumbnail" in result
        assert "url" in result
        assert "height" in result
        assert "width" in result
        assert "source" in result
        
def test_image_search_max_results(rate_limit_delay):
    payload = {"keywords": "nature", "max_results": 5}
    response = requests.post(f"{BASE_URL}/images", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 5
    
def test_image_search_invalid_safesearch(rate_limit_delay):
    payload = {"keywords": "nature", "safesearch": "invalid"}
    response = requests.post(f"{BASE_URL}/images", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_image_search_empty_keywords(rate_limit_delay):
    payload = {"keywords": ""}
    response = requests.post(f"{BASE_URL}/images", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_video_search_success(rate_limit_delay):
    payload = {"keywords": "python tutorial"}
    response = requests.post(f"{BASE_URL}/videos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    for result in data["results"]:
        assert "content" in result
        assert "title" in result
        
def test_video_search_max_results(rate_limit_delay):
    payload = {"keywords": "python tutorial", "max_results": 3}
    response = requests.post(f"{BASE_URL}/videos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 3
    
def test_video_search_invalid_safesearch(rate_limit_delay):
    payload = {"keywords": "python tutorial", "safesearch": "invalid"}
    response = requests.post(f"{BASE_URL}/videos", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_video_search_empty_keywords(rate_limit_delay):
    payload = {"keywords": ""}
    response = requests.post(f"{BASE_URL}/videos", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_news_search_success(rate_limit_delay):
    payload = {"keywords": "technology"}
    response = requests.post(f"{BASE_URL}/news", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    for result in data["results"]:
        assert "date" in result
        assert "title" in result
        assert "body" in result
        assert "url" in result
        assert "source" in result
        
def test_news_search_max_results(rate_limit_delay):
    payload = {"keywords": "technology", "max_results": 4}
    response = requests.post(f"{BASE_URL}/news", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 4
    
def test_news_search_invalid_safesearch(rate_limit_delay):
    payload = {"keywords": "technology", "safesearch": "invalid"}
    response = requests.post(f"{BASE_URL}/news", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
def test_news_search_empty_keywords(rate_limit_delay):
    payload = {"keywords": ""}
    response = requests.post(f"{BASE_URL}/news", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data