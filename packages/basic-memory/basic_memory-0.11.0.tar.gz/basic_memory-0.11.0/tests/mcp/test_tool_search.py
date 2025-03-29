"""Tests for search MCP tools."""

import pytest
from datetime import datetime, timedelta

from basic_memory.mcp.tools import write_note
from basic_memory.mcp.tools.search import search_notes
from basic_memory.schemas.search import SearchQuery, SearchItemType


@pytest.mark.asyncio
async def test_search_basic(client):
    """Test basic search functionality."""
    # Create a test note
    result = await write_note(
        title="Test Search Note",
        folder="test",
        content="# Test\nThis is a searchable test note",
        tags=["test", "search"],
    )
    assert result

    # Search for it
    query = SearchQuery(text="searchable")
    response = await search_notes(query)

    # Verify results
    assert len(response.results) > 0
    assert any(r.permalink == "test/test-search-note" for r in response.results)


@pytest.mark.asyncio
async def test_search_pagination(client):
    """Test basic search functionality."""
    # Create a test note
    result = await write_note(
        title="Test Search Note",
        folder="test",
        content="# Test\nThis is a searchable test note",
        tags=["test", "search"],
    )
    assert result

    # Search for it
    query = SearchQuery(text="searchable")
    response = await search_notes(query, page=1, page_size=1)

    # Verify results
    assert len(response.results) == 1
    assert any(r.permalink == "test/test-search-note" for r in response.results)


@pytest.mark.asyncio
async def test_search_with_type_filter(client):
    """Test search with entity type filter."""
    # Create test content
    await write_note(
        title="Entity Type Test",
        folder="test",
        content="# Test\nFiltered by type",
    )

    # Search with type filter
    query = SearchQuery(text="type", types=[SearchItemType.ENTITY])
    response = await search_notes(query)

    # Verify all results are entities
    assert all(r.type == "entity" for r in response.results)


@pytest.mark.asyncio
async def test_search_with_date_filter(client):
    """Test search with date filter."""
    # Create test content
    await write_note(
        title="Recent Note",
        folder="test",
        content="# Test\nRecent content",
    )

    # Search with date filter
    one_hour_ago = datetime.now() - timedelta(hours=1)
    query = SearchQuery(text="recent", after_date=one_hour_ago)
    response = await search_notes(query)

    # Verify we get results within timeframe
    assert len(response.results) > 0
