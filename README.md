# Fantasy Football Draft Assistant MCP Server

A Python-based Model Context Protocol (MCP) server that provides comprehensive fantasy football data and insights to Claude Desktop. This server scrapes data from various sources, caches it efficiently, and exposes multiple tools for fantasy football draft analysis and decision-making.

## Overview

This MCP server is designed to be integrated with Claude Desktop, providing real-time access to fantasy football data including injuries, player stats, rankings, and more. It uses a modular architecture with separation of concerns, making it easy to extend with additional data sources and tools for comprehensive fantasy football analysis.

## Tools & Resources Exposed

### `get_nfl_injuries`
- **Type**: Tool
- **Description**: Retrieves the latest NFL injuries data, using cached data if available (refreshed every 24 hours)
- **Returns**: List of injury reports by team with player details, injury status, and dates
- **Data Source**: ESPN NFL Injuries Page

### `get_player_ratings`
- **Type**: Tool
- **Description**: Retrieves all player ratings from multiple sources (cached, refreshed every 48 hours)
- **Returns**: List of player ratings with name, position, team, overall rating, and source
- **Data Source**: Madden NFL Ratings (EA Sports)

### `get_player_ratings_by_source`
- **Type**: Tool
- **Description**: Filters player ratings by specific source (e.g., 'Madden NFL')
- **Parameters**: `source` (string) - The data source to filter by
- **Returns**: Filtered list of player ratings from the specified source

### `get_player_ratings_by_position`
- **Type**: Tool
- **Description**: Filters player ratings by position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DEF')
- **Parameters**: `position` (string) - The position to filter by
- **Returns**: Filtered list of player ratings for the specified position

### `get_player_ratings_by_team`
- **Type**: Tool
- **Description**: Filters player ratings by team name
- **Parameters**: `team` (string) - The team name to filter by
- **Returns**: Filtered list of player ratings for the specified team

## Data Sources

### ESPN NFL Injuries
- **URL**: https://www.espn.com/nfl/injuries
- **Data**: Player injury reports, status, and dates
- **Cache TTL**: 24 hours
- **Use Case**: Injury analysis for fantasy football draft decisions

### Madden NFL Ratings (EA Sports)
- **URL**: https://www.ea.com/games/madden-nfl/ratings
- **Data**: Player overall ratings, positions, teams
- **Cache TTL**: 48 hours
- **Use Case**: Player performance assessment and draft rankings

## Architecture & Tooling

### Project Structure
```
pigskin-pickem/
├── app/
│   ├── __init__.py
│   ├── server.py              # FastMCP server with tool definitions
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── nfl_injuries.py    # ESPN injuries scraper
│   │   └── madden_ratings.py  # Madden ratings scraper
│   ├── cache/
│   │   ├── __init__.py
│   │   └── cache.py           # Generic caching system
│   └── resources/
│       ├── __init__.py
│       ├── nfl_injuries_resource.py
│       └── player_ratings_resource.py
├── tests/
│   ├── test_scraper.py
│   ├── test_cache.py
│   ├── test_resource.py
│   ├── test_madden_ratings.py
│   └── test_player_ratings_resource.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

### Key Components
- **FastMCP**: Modern MCP server framework for Claude Desktop integration
- **Modular Scrapers**: Separate modules for each data source with error handling and logging
- **Caching System**: File-based caching with configurable TTL for each data type
- **Resource Layer**: Abstraction layer between scrapers and MCP tools
- **Comprehensive Testing**: Pytest-based tests with mocking for all components

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip3
- Virtual environment (recommended)

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pigskin-pickem
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Claude Desktop Integration
Add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "FantasyFootballAssistant": {
      "command": "/usr/bin/python3",
      "args": [
        "app/server.py"
      ],
      "cwd": "/path/to/pigskin-pickem"
    }
  }
}
```

### MCP Inspector Testing
To test your MCP server using the official MCP Inspector tool:

1. **Install the MCP Inspector** (if not already installed):
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **Launch the Inspector** from the project root:
   ```bash
   npx @modelcontextprotocol/inspector /Users/todd/code/pigskin-pickem/v5/venv/bin/python -m app.server
   ```

3. **Alternative: Use the wrapper script** (recommended for better compatibility):
   ```bash
   npx @modelcontextprotocol/inspector
   ```
   Then in the web interface, configure:
   - **Command:** `python`
   - **Arguments:** `mcp_server_wrapper.py`
   - **Working Directory:** `/Users/todd/code/pigskin-pickem/v5`
   - **Environment Variables:** `PYTHONPATH=.`

The MCP Inspector provides a web-based interface for testing all your fantasy football tools interactively, including:
- `get_nfl_injuries()`
- `get_player_ratings()`
- `get_player_ratings_by_source(source)`
- `get_player_ratings_by_position(position)`
- `get_player_ratings_by_team(team)`

For detailed instructions, see `MCP_INSPECTOR_GUIDE.md`.

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test categories:
```bash
pytest tests/test_scraper.py      # Scraper tests
pytest tests/test_cache.py        # Cache tests
pytest tests/test_resource.py     # Resource tests
pytest tests/test_madden_ratings.py  # Madden ratings tests
```

### Run with verbose output:
```bash
pytest -v
```

## Usage Examples

### Getting NFL Injuries
```python
# Get all current injuries
injuries = await get_nfl_injuries()
```

### Getting Player Ratings
```python
# Get all player ratings
ratings = await get_player_ratings()

# Get ratings by position
qb_ratings = await get_player_ratings_by_position("QB")
rb_ratings = await get_player_ratings_by_position("RB")

# Get ratings by team
chiefs_ratings = await get_player_ratings_by_team("Kansas City Chiefs")

# Get ratings by source
madden_ratings = await get_player_ratings_by_source("Madden NFL")
```

### Fantasy Football Analysis
```python
# Example: Find top QBs by rating
qb_ratings = await get_player_ratings_by_position("QB")
top_qbs = sorted(qb_ratings, key=lambda x: x["overall"], reverse=True)[:5]

# Example: Check injuries for a specific team
injuries = await get_nfl_injuries()
team_injuries = [i for i in injuries if i["team"] == "Kansas City Chiefs"]
```

## Data Structure Examples

### NFL Injuries Response
```json
[
  {
    "team": "Kansas City Chiefs",
    "injuries": [
      {
        "player": "Patrick Mahomes",
        "position": "QB",
        "injury": "Ankle",
        "status": "Questionable",
        "date": "2024-01-15"
      }
    ]
  }
]
```

### Player Ratings Response
```json
[
  {
    "name": "Patrick Mahomes",
    "position": "QB",
    "team": "Kansas City Chiefs",
    "overall": 95,
    "source": "Madden NFL"
  }
]
```

## Development

### Adding New Data Sources
1. Create a new scraper in `app/scraper/`
2. Add cache functions in `app/cache/cache.py`
3. Create a resource module in `app/resources/`
4. Add tools to `app/server.py`
5. Write comprehensive tests

### Adding New Tools
1. Define the tool function in `app/server.py`
2. Add appropriate logging and error handling
3. Write tests for the new functionality
4. Update documentation

## Future Enhancements

### Planned Features
- **ADP (Average Draft Position) Data**: Integration with fantasy football platforms
- **Player Statistics**: Historical and current season stats
- **Draft Strategy Tools**: AI-powered draft recommendations
- **League-Specific Analysis**: Custom scoring system support
- **Real-Time Updates**: WebSocket-based live data updates
- **Additional Data Sources**: PFF, FantasyPros, NFL.com integration

### Data Sources to Add
- **FantasyPros**: ADP and expert rankings
- **Pro Football Focus**: Advanced analytics and grades
- **NFL.com**: Official statistics and news
- **ESPN Fantasy**: Fantasy-specific data and projections

## Error Handling & Logging

The server includes comprehensive error handling and logging:
- **Network Errors**: Graceful handling of HTTP request failures
- **Parsing Errors**: Robust HTML parsing with fallback mechanisms
- **Cache Errors**: File system error handling for cache operations
- **Logging**: Structured logging for debugging and monitoring

## Cache Management

- **Location**: `/tmp/pigskin-pickem-cache/`
- **Files**: Separate cache files for each data type
- **TTL**: Configurable time-to-live for each data source
- **Persistence**: Cache persists between server restarts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the test examples
