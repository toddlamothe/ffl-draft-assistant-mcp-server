# Fantasy Football Draft Assistant MCP Server

A Python-based Model Context Protocol (MCP) server that provides comprehensive fantasy football data and insights to Claude Desktop. This server scrapes data from various sources, caches it efficiently, and exposes multiple tools for fantasy football draft analysis and decision-making.

## Overview

This MCP server is designed to be integrated with Claude Desktop, providing real-time access to fantasy football data including injuries, player stats, rankings, and more. It uses a modular architecture with separation of concerns, making it easy to extend with additional data sources and tools for comprehensive fantasy football assistance.

## Tools & Resources Exposed

### `get_nfl_injuries`
- **Type**: Tool
- **Description**: Retrieves the latest NFL injuries data, using cached data if available (refreshed every 24 hours)
- **Use Case**: Injury analysis for draft decisions and roster management
- **Returns**: List of team injury reports with player details
- **Data Structure**: 
  ```json
  [
    {
      "team": "Team Name",
      "injuries": [
        {
          "player": "Player Name",
          "position": "Position",
          "injury": "Injury Description",
          "status": "Status (Out, Questionable, etc.)",
          "date": "Date"
        }
      ]
    }
  ]
  ```

*More tools and resources will be added as the project evolves, including player rankings, statistics, ADP data, and more.*

## Data Sources

### ESPN NFL Injuries
- **URL**: https://www.espn.com/nfl/injuries
- **Frequency**: Scraped on-demand, cached for 24 hours
- **Data**: Team-by-team injury reports with player details, positions, injury descriptions, and status
- **Fantasy Impact**: Critical for draft decisions and understanding player availability

*Additional data sources will be integrated for comprehensive fantasy football analysis.*

## Tooling & Architecture Overview

### Project Structure
```
pigskin-pickem/
├── app/
│   ├── __init__.py
│   ├── server.py              # FastMCP server entry point
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── nfl_injuries.py    # ESPN scraping logic
│   ├── cache/
│   │   ├── __init__.py
│   │   └── cache.py           # File-based caching system
│   └── resources/
│       ├── __init__.py
│       └── nfl_injuries_resource.py  # Resource abstraction layer
├── tests/
│   ├── test_scraper.py        # Scraper unit tests
│   ├── test_cache.py          # Cache unit tests
│   └── test_resource.py       # Resource unit tests
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
├── pytest.ini               # Pytest configuration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Architecture Components

1. **FastMCP Server** (`app/server.py`)
   - Main MCP server using FastMCP framework
   - Exposes fantasy football tools for Claude Desktop integration
   - Handles MCP protocol communication

2. **Scraper Module** (`app/scraper/`)
   - Modular web scraping logic for multiple data sources
   - Uses `httpx` for HTTP requests and `beautifulsoup4` for HTML parsing
   - Designed for easy extension to additional fantasy football data sources

3. **Cache Module** (`app/cache/`)
   - File-based caching system with configurable TTL
   - Stores data in `/tmp/pigskin-pickem-cache/` for persistence across sessions
   - Automatic cache invalidation and refresh

4. **Resource Layer** (`app/resources/`)
   - Abstraction layer between server and data sources
   - Handles cache logic and data fetching coordination
   - Provides clean interface for fantasy football tools

## Installation & Setup

### Prerequisites
- Python 3.10 or later
- pip3

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pigskin-pickem/v5
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Claude Desktop Integration

1. **Locate Claude Desktop config file**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add MCP server configuration**
   ```json
   {
     "mcpServers": {
       "FantasyFootballAssistant": {
         "command": [
           "python3",
           "app/server.py"
         ],
         "cwd": "/path/to/your/pigskin-pickem/v5"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test files
```bash
pytest tests/test_scraper.py
pytest tests/test_cache.py
pytest tests/test_resource.py
```

### Test with verbose output
```bash
pytest -v
```

## Usage

### Manual Server Execution
```bash
python3 app/server.py
```

### Fantasy Football Draft Assistance
Once integrated with Claude Desktop, you can ask Claude to:
- "Get the latest NFL injuries for draft analysis"
- "Show me all injured running backs and their status"
- "Which teams have the most injuries affecting fantasy-relevant players?"
- "What's the injury status for [player name] and how does it affect their draft value?"
- *Future capabilities will include:*
  - Player rankings and ADP analysis
  - Statistical projections
  - Draft strategy recommendations
  - Team-by-team depth chart analysis
  - Sleepers and busts identification

## Development

### Adding New Data Sources
1. Create a new scraper in `app/scraper/`
2. Add corresponding cache logic if needed
3. Create a resource wrapper in `app/resources/`
4. Add the tool/resource to `app/server.py`
5. Write tests in `tests/`

### Adding New Fantasy Football Tools/Resources
1. Define the tool using `@mcp.tool()` decorator in `app/server.py`
2. Implement the logic using existing modules
3. Add comprehensive tests
4. Update this README with new tool documentation

### Planned Features
- Player rankings and ADP data
- Statistical projections and analysis
- Draft strategy tools
- Team depth charts
- Player news and updates
- Trade value calculators
- Waiver wire recommendations

## Dependencies

### Core Dependencies
- `fastmcp`: MCP server framework
- `httpx`: HTTP client for web scraping
- `beautifulsoup4`: HTML parsing
- `fastapi`: Web framework (used by FastMCP)
- `uvicorn`: ASGI server

### Development Dependencies
- `pytest`: Testing framework

## Caching Strategy

- **Location**: `/tmp/pigskin-pickem-cache/`
- **TTL**: Configurable per data source (24 hours for injuries)
- **Persistence**: Survives between Claude Desktop sessions
- **Fallback**: Fresh data fetch if cache is expired or missing

## Error Handling

The server includes robust error handling for:
- Network failures during scraping
- Cache file corruption
- Invalid HTML responses
- Missing data fields
- Rate limiting from data sources

## Contributing

1. Follow the existing modular architecture
2. Add tests for new functionality
3. Update this README for new features
4. Ensure all tests pass before submitting
5. Focus on fantasy football relevance and utility

## License

[Add your license information here]

## Support

For issues or questions, please [create an issue](link-to-issues) or contact [your contact information].
