#!/usr/bin/env python3
"""
Test script for the Fantasy Football MCP Server
This script tests the underlying functions that the MCP server uses.
"""

import asyncio
import json
import logging
import pytest
from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from app.resources.player_ratings_resource import (
    get_all_player_ratings, 
    get_player_ratings_by_source,
    get_player_ratings_by_position,
    get_player_ratings_by_team
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_mcp_functions():
    """Test all the functions that the MCP server uses."""
    
    print("🧪 Testing Fantasy Football MCP Server Functions...")
    print("=" * 50)
    
    # Test 1: NFL Injuries
    print("\n1. Testing NFL injuries functionality...")
    try:
        injuries = get_cache()
        if injuries is None:
            print("   Cache miss, fetching fresh injuries...")
            injuries = fetch_nfl_injuries()
            set_cache(injuries)
        print(f"✅ Success! Retrieved {len(injuries)} injury records")
        if injuries:
            print(f"   Sample injury: {injuries[0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: All Player Ratings
    print("\n2. Testing get_all_player_ratings()...")
    try:
        ratings = get_all_player_ratings()
        print(f"✅ Success! Retrieved {len(ratings)} player ratings")
        if ratings:
            print(f"   Sample rating: {ratings[0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Player Ratings by Source
    print("\n3. Testing get_player_ratings_by_source('Madden NFL')...")
    try:
        madden_ratings = get_player_ratings_by_source("Madden NFL")
        print(f"✅ Success! Retrieved {len(madden_ratings)} Madden ratings")
        if madden_ratings:
            print(f"   Sample Madden rating: {madden_ratings[0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Player Ratings by Position
    print("\n4. Testing get_player_ratings_by_position('QB')...")
    try:
        qb_ratings = get_player_ratings_by_position("QB")
        print(f"✅ Success! Retrieved {len(qb_ratings)} QB ratings")
        if qb_ratings:
            print(f"   Sample QB rating: {qb_ratings[0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Player Ratings by Team
    print("\n5. Testing get_player_ratings_by_team('Kansas City Chiefs')...")
    try:
        chiefs_ratings = get_player_ratings_by_team("Kansas City Chiefs")
        print(f"✅ Success! Retrieved {len(chiefs_ratings)} Chiefs ratings")
        if chiefs_ratings:
            print(f"   Sample Chiefs rating: {chiefs_ratings[0]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server function testing complete!")

def test_mcp_server_startup():
    """Test that the MCP server can start up properly."""
    print("\n🔧 Testing MCP server startup...")
    try:
        # Import the server module to check for syntax errors
        import app.server
        print("✅ MCP server module imports successfully")
        
        # Check that the FastMCP instance exists
        if hasattr(app.server, 'mcp'):
            print("✅ FastMCP instance created successfully")
        else:
            print("❌ FastMCP instance not found")
            
    except Exception as e:
        print(f"❌ Error importing MCP server: {e}")

if __name__ == "__main__":
    # Test the MCP server startup first
    test_mcp_server_startup()
    
    # Then test the underlying functions
    asyncio.run(test_mcp_functions())
