import pytest
import asyncio
from unittest.mock import AsyncMock
from src.asyncddgs.async_ddgs import aDDGS

@pytest.mark.asyncio
async def test_text_search(mocker):
    """Test text search with mocked API response."""
    mock_ddgs = aDDGS()
    mock_response = [{"title": "Python", "href": "https://www.python.org", "body": "Python programming language"}]
    mocker.patch.object(mock_ddgs, "text", AsyncMock(return_value=mock_response))
    
    results = await mock_ddgs.text("python programming")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "href" in results[0]
    assert "body" in results[0]

@pytest.mark.asyncio
async def test_image_search(mocker):
    """Test image search with mocked API response."""
    mock_ddgs = aDDGS()
    mock_response = [{"title": "Image", "image": "https://example.com/image.jpg", "url": "https://example.com"}]
    mocker.patch.object(mock_ddgs, "images", AsyncMock(return_value=mock_response))
    
    results = await mock_ddgs.images("nature")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "image" in results[0]
    assert "url" in results[0]

@pytest.mark.asyncio
async def test_video_search(mocker):
    """Test video search with mocked API response."""
    mock_ddgs = aDDGS()
    mock_response = [{"title": "Video", "content": "https://example.com/video.mp4"}]
    mocker.patch.object(mock_ddgs, "videos", AsyncMock(return_value=mock_response))
    
    results = await mock_ddgs.videos("python tutorial")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "content" in results[0]

@pytest.mark.asyncio
async def test_news_search(mocker):
    """Test news search with mocked API response."""
    mock_ddgs = aDDGS()
    mock_response = [{"title": "News", "url": "https://example.com/news", "source": "Example News"}]
    mocker.patch.object(mock_ddgs, "news", AsyncMock(return_value=mock_response))
    
    results = await mock_ddgs.news("technology")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]
    assert "source" in results[0]
