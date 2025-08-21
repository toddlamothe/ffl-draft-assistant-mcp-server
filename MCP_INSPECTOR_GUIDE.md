# MCP Inspector Guide for Fantasy Football Server

## 🚨 Problem Solved: `--directory` Error

The error `unknown option --directory` occurs because the MCP Inspector tries to pass arguments that your FastMCP server doesn't recognize. I've created a wrapper script to handle this.

## 🛠️ Solution: Use the Wrapper Script

### Option 1: Use the Wrapper Script (Recommended)

In the MCP Inspector, configure your server with:

**Command:** `python`  
**Arguments:** `mcp_server_wrapper.py`  
**Working Directory:** `/Users/todd/code/pigskin-pickem/v5`  
**Environment Variables:** `PYTHONPATH=.`

### Option 2: Use the Modified Server

**Command:** `python`  
**Arguments:** `app/server_with_args.py`  
**Working Directory:** `/Users/todd/code/pigskin-pickem/v5`  
**Environment Variables:** `PYTHONPATH=.`

## 📋 Step-by-Step Instructions

### 1. Start the MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```

### 2. Configure Your Server

In the web interface that opens:

1. **Server Name:** `fantasy-football-assistant`
2. **Command:** `python`
3. **Arguments:** `mcp_server_wrapper.py`
4. **Working Directory:** `/Users/todd/code/pigskin-pickem/v5`
5. **Environment Variables:**
   ```
   PYTHONPATH=.
   ```

### 3. Connect and Test

Click "Connect" and you should see your 5 fantasy football tools:

- `get_nfl_injuries()`
- `get_player_ratings()`
- `get_player_ratings_by_source(source)`
- `get_player_ratings_by_position(position)`
- `get_player_ratings_by_team(team)`

## 🧪 Testing Your Tools

### Test 1: NFL Injuries
```json
{
  "name": "get_nfl_injuries",
  "arguments": {}
}
```

### Test 2: Player Ratings by Position
```json
{
  "name": "get_player_ratings_by_position",
  "arguments": {
    "position": "QB"
  }
}
```

### Test 3: Player Ratings by Team
```json
{
  "name": "get_player_ratings_by_team",
  "arguments": {
    "team": "Kansas City Chiefs"
  }
}
```

### Test 4: Player Ratings by Source
```json
{
  "name": "get_player_ratings_by_source",
  "arguments": {
    "source": "Madden NFL"
  }
}
```

## 🔧 Troubleshooting

### Common Issues

1. **"Command not found"**
   - Ensure your virtual environment is activated
   - Verify Python is in your PATH

2. **Import errors**
   - Check that `PYTHONPATH=.` is set
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **Connection refused**
   - The inspector should manage the server process automatically
   - Check the inspector logs for startup errors

4. **Still getting `--directory` error**
   - Make sure you're using `mcp_server_wrapper.py` as the argument
   - Verify the wrapper script is executable: `chmod +x mcp_server_wrapper.py`

### Debug Mode

To see more detailed logs, add `--verbose` to the arguments:

**Arguments:** `mcp_server_wrapper.py --verbose`

## 📁 Files Created

- `mcp_server_wrapper.py` - Handles MCP inspector arguments
- `app/server_with_args.py` - Modified server with argument parsing
- `MCP_INSPECTOR_GUIDE.md` - This guide

## 🎯 Benefits of MCP Inspector

1. **Visual Interface** - Web-based UI for testing
2. **Real-time Testing** - Test tools without writing code
3. **Protocol Validation** - Ensures your server follows MCP spec
4. **Debugging** - See exactly what's being sent/received
5. **Documentation** - View tool schemas and descriptions

## 🔄 Alternative: Cursor Testing

If you prefer to test in Cursor instead:

1. Use the `cursor-mcp-config.json` configuration
2. Run `./start_mcp_server.sh`
3. Connect via Cursor's MCP extension

## 🎉 Success Indicators

When working correctly, you should see:

- ✅ Server connects without errors
- ✅ All 5 tools listed in the interface
- ✅ Tool calls return data (NFL injuries, player ratings, etc.)
- ✅ No `--directory` or other argument errors

## 📞 Support

If you continue to have issues:

1. Check the inspector's console logs
2. Verify your virtual environment is activated
3. Test the wrapper locally: `python mcp_server_wrapper.py --help`
4. Ensure all dependencies are installed correctly
