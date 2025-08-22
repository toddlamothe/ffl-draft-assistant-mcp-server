# Data Directory

This directory contains data files used by the Fantasy Football MCP server.

## PFF Ratings CSV File

### File Location
Place your Pro Football Focus (PFF) player ratings CSV file at:
```
data/pff_ratings.csv
```

### Expected CSV Format

Your CSV file should have the following columns (column names are flexible):

| Column | Description | Example |
|--------|-------------|---------|
| `name` | Player name | "Patrick Mahomes" |
| `position` | Player position | "QB", "RB", "WR", "TE" |
| `team` | Team name | "Kansas City Chiefs" |
| `overall` | Overall rating | 99 |
| `grade` | PFF grade | 92.5 |
| `rank` | Position rank | 1 |
| `snaps` | Total snaps played | 1056 |
| `games` | Games played | 17 |

### Supported Column Name Variations

The system is flexible and will recognize these column name variations:

- **Player Name**: `name`, `player`, `player_name`
- **Position**: `position`, `pos`
- **Team**: `team`, `team_name`
- **Overall Rating**: `overall`, `rating`, `grade`
- **PFF Grade**: `grade`, `pff_grade`
- **Rank**: `rank`, `position_rank`
- **Snaps**: `snaps`, `total_snaps`
- **Games**: `games`, `games_played`

### Example CSV Content

```csv
name,position,team,overall,grade,rank,snaps,games
Patrick Mahomes,QB,Kansas City Chiefs,99,92.5,1,1056,17
Josh Allen,QB,Buffalo Bills,98,89.2,2,1089,17
Christian McCaffrey,RB,San Francisco 49ers,97,91.3,1,789,17
Tyreek Hill,WR,Miami Dolphins,95,90.1,1,1023,17
Travis Kelce,TE,Kansas City Chiefs,96,91.8,1,789,17
```

## How to Use

1. **Download your PFF ratings** from Pro Football Focus
2. **Save as CSV** with the column structure above
3. **Rename to `pff_ratings.csv`**
4. **Place in this directory** (`data/pff_ratings.csv`)
5. **Restart your MCP server** to load the new data

## Available MCP Tools

Once your CSV is in place, these MCP tools will be available:

- `get_pff_ratings()` - Get all PFF ratings
- `get_pff_ratings_by_position(position)` - Filter by position
- `get_pff_ratings_by_team(team)` - Filter by team
- `get_pff_ratings_by_grade_range(min_grade, max_grade)` - Filter by grade range
- `get_top_pff_ratings_by_position(position, top_n)` - Get top N players by position
- `get_pff_player_by_name(player_name)` - Get specific player
- `get_pff_stats()` - Get dataset statistics

## Troubleshooting

### File Not Found Error
If you see "PFF ratings file not found", make sure:
- File is named exactly `pff_ratings.csv`
- File is in the `data/` directory
- File has proper read permissions

### Data Loading Issues
If data doesn't load properly:
- Check CSV format matches expected structure
- Ensure no empty rows or malformed data
- Verify column names are recognized

### Performance
- Large CSV files (>10,000 rows) may take a moment to load
- Data is loaded fresh each time (no caching for CSV data)
- Consider filtering data if file is very large
