# MCP Tools Reference for Fantasy Football Draft Assistant

## Available Tools

### 1. `get_nfl_injuries()`
**Purpose**: Get latest NFL injury data
**Returns**: List of teams with injury details
**Use Case**: Check for QB/OL injuries that affect player value
**Cache**: 24-hour TTL

**Response Format**:
```json
[
  {
    "team": "Kansas City Chiefs",
    "injuries": [
      {
        "player": "Patrick Mahomes",
        "position": "QB",
        "estimated_return_date": "Sep 7",
        "status": "Questionable",
        "status_update": "Recent status update..."
      }
    ]
  }
]
```

### 2. `get_player_ratings()`
**Purpose**: Get all player ratings from multiple sources (Madden NFL + PFF) with unified format
**Returns**: Complete list of players with ratings from all available sources
**Use Case**: Comprehensive player analysis with multiple rating sources
**Cache**: 48-hour TTL

**Response Format**:
```json
[
  {
    "name": "Patrick Mahomes",
    "position": "QB",
    "team": "Kansas City Chiefs",
    "ratings": [
      {
        "source": "Madden NFL",
        "overall": 99,
        "attributes": {
          "throw_power": 97,
          "throw_accuracy": 95,
          "speed": 84
        },
        "position_rank": 1
      },
      {
        "source": "Pro Football Focus",
        "overall": null,
        "pff_grade": 92.5,
        "pff_rank": 1,
        "overall_rank": 1,
        "position_rank": 1,
        "projected_points": 350.2,
        "adp": 2.1,
        "auction_value": 65.0,
        "bye_week": 10
      }
    ]
  }
]
```

### 3. `get_player_ratings_by_position(position)`
**Purpose**: Filter ratings by position (QB, RB, WR, TE, K, DEF) with ratings from all sources
**Parameters**: `position` (string) - Position to filter
**Use Case**: Position-specific analysis with multiple rating sources
**Example**: `get_player_ratings_by_position("QB")`

### 4. `get_player_ratings_by_team(team)`
**Purpose**: Filter ratings by team name with ratings from all sources
**Parameters**: `team` (string) - Full team name
**Use Case**: Team context analysis with multiple rating sources
**Example**: `get_player_ratings_by_team("Kansas City Chiefs")`

### 5. `get_player_ratings_by_source(source)`
**Purpose**: Filter ratings by source (e.g., "Madden NFL", "Pro Football Focus")
**Parameters**: `source` (string) - Rating source
**Use Case**: Source-specific analysis
**Example**: `get_player_ratings_by_source("Madden NFL")`

### 6. `get_player_ratings_stats()`
**Purpose**: Get statistics about the combined player ratings dataset (Madden + PFF)
**Returns**: Dataset statistics and coverage information
**Use Case**: Understanding data coverage and quality
**Example**: `get_player_ratings_stats()`

### 7. `get_ol_rankings()`
**Purpose**: Get all PFF offensive line rankings
**Returns**: Complete list of team OL rankings
**Use Case**: Offensive line analysis for RB/QB evaluation
**Cache**: 48-hour TTL
**Data Source**: Scraped from [PFF OL Rankings](https://www.pff.com/news/nfl-2025-nfl-offensive-line-rankings)

**Response Format**:
```json
[
  {
    "rank": 1,
    "team": "Philadelphia Eagles",
    "description": "The Eagles boast the NFL's best offensive tackle duo...",
    "key_details": {
      "pff_overall_grade": 95.2,
      "pff_pass_blocking_grade": 88.9,
      "pressures_allowed": 110,
      "sacks_allowed": 6
    }
  }
]
```

### 8. `get_ol_rankings_by_team(team)`
**Purpose**: Get offensive line ranking for specific team
**Parameters**: `team` (string) - Team name
**Use Case**: Team-specific OL analysis
**Example**: `get_ol_rankings_by_team("Philadelphia Eagles")`

### 9. `get_top_ol_rankings(top_n)`
**Purpose**: Get top N offensive line rankings
**Parameters**: `top_n` (int) - Number of top teams to return
**Use Case**: Identify teams with best offensive lines
**Example**: `get_top_ol_rankings(10)`

### 10. `get_ol_rankings_by_rank_range(min_rank, max_rank)`
**Purpose**: Get OL rankings within specific rank range
**Parameters**: 
- `min_rank` (int) - Minimum rank
- `max_rank` (int) - Maximum rank
**Use Case**: Find teams with OL in specific tier
**Example**: `get_ol_rankings_by_rank_range(1, 10)`

### 11. `get_ol_rankings_stats()`
**Purpose**: Get statistics about OL rankings dataset
**Returns**: Dataset statistics and distribution
**Use Case**: Understanding OL ranking coverage
**Example**: `get_ol_rankings_stats()`

## Usage Strategy

### For Player Analysis:
1. **Start with**: `get_player_ratings_by_position()` to get position context with all sources
2. **Add team context**: `get_player_ratings_by_team()` for offensive scheme analysis
3. **Check OL quality**: `get_ol_rankings_by_team()` for offensive line analysis
4. **Check injuries**: `get_nfl_injuries()` for QB/OL injury impact
5. **Compare sources**: Use unified ratings to compare Madden vs PFF assessments

### For Draft Strategy:
1. **Position runs**: Use `get_player_ratings_by_position()` to see available players with all ratings
2. **Elite players**: Use `get_player_ratings_by_source("Pro Football Focus")` to identify top PFF performers
3. **Team stacks**: Use `get_player_ratings_by_team()` to evaluate QB-WR/TE combinations
4. **OL analysis**: Use `get_ol_rankings_by_team()` to evaluate offensive line quality
5. **Injury monitoring**: Use `get_nfl_injuries()` to identify value opportunities
6. **Source comparison**: Use `get_player_ratings_by_source()` for source-specific analysis

### For Value Assessment:
1. **Overall rankings**: Use `get_player_ratings()` for complete picture with all sources
2. **Advanced metrics**: Use PFF data within unified ratings for deeper analytics
3. **OL context**: Use `get_ol_rankings()` to evaluate blocking quality
4. **Position scarcity**: Compare position groups using position filters
5. **Team context**: Use team filters for scheme analysis

## Key Data Points to Extract

### Player Ratings (Unified):
- **Overall Rating**: Primary value indicator from Madden
- **PFF Grade**: Advanced performance metric from PFF
- **Position Rank**: Scarcity assessment from both sources
- **Team**: Offensive scheme context
- **Projected Points**: PFF fantasy projections
- **ADP**: Average draft position from PFF
- **Auction Value**: PFF auction values

### Offensive Line Rankings:
- **OL Rank**: Team offensive line quality (1-32)
- **PFF Grades**: Individual OL player grades
- **Pressure Stats**: Sacks and pressures allowed
- **Pass Blocking Efficiency**: Advanced blocking metrics

### Injury Data:
- **QB Injuries**: Direct impact on WR/TE value
- **OL Injuries**: Impact on RB/QB performance
- **Return Timeline**: Risk assessment
- **Status**: Severity indication

### Team Analysis:
- **Player Distribution**: Depth chart analysis
- **Rating Spread**: Team strength assessment
- **Position Groups**: Offensive weapon evaluation
- **OL Quality**: Blocking unit assessment

## Integration Tips

1. **Always check injuries first** - QB/OL injuries can dramatically change player value
2. **Compare Madden vs PFF** - Use unified ratings to see both perspectives
3. **Focus on PFF grades** - More sophisticated than simple overall ratings
4. **Consider OL quality** - Use `get_ol_rankings_by_team()` for RB/QB analysis
5. **Consider volume metrics** - Snaps and games played indicate consistency
6. **Cross-reference data** - Combine multiple tools for comprehensive analysis
7. **Focus on PPR impact** - Prioritize players with reception potential

## Example Workflow

```
1. User asks: "Should I draft Christian McCaffrey?"
2. Use get_player_ratings_by_position("RB") to see RB landscape with all ratings
3. Use get_player_ratings_by_team("SF") for team context and find McCaffrey
4. Use get_ol_rankings_by_team("San Francisco 49ers") for OL analysis
5. Use get_nfl_injuries() to check for 49ers OL injuries
6. Combine Madden ratings + PFF grades + OL quality + injury data
7. Provide PPR-specific recommendation
```

## Data Coverage

The unified system provides:
- **2,426 unique players** with ratings from multiple sources
- **2,368 Madden ratings** with overall scores and attributes
- **512 PFF ratings** with advanced metrics and fantasy projections
- **32 team OL rankings** with detailed blocking analysis
- **Real-time injury data** updated every 24 hours

This comprehensive dataset allows for sophisticated fantasy football analysis combining traditional ratings, advanced analytics, and contextual team information.
