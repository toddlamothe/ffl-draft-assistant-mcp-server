# Quick Setup Guide for Claude Desktop

## Step 1: Start Your MCP Server

```bash
# From your project directory
python app/server.py
```

**Keep this running** - Claude Desktop needs the server to be active.

## Step 2: Configure Claude Desktop

1. **Open Claude Desktop**
2. **Go to Settings** (gear icon)
3. **Click "Custom Instructions"**
4. **Copy the entire content** from `fantasy_football_draft_assistant_prompt.md`
5. **Paste it** into the Custom Instructions field
6. **Save** the settings

## Step 3: Verify MCP Connection

1. **Start a new conversation** in Claude Desktop
2. **Ask**: "What MCP tools are available?"
3. **Claude should respond** with the available tools from your server

## Step 4: Test the Setup

**Try this test question:**
```
"Should I draft Christian McCaffrey in a PPR league?"
```

**Expected response:**
- Claude should use your MCP server data
- Provide structured analysis with ratings
- Give PPR-specific recommendations
- Include draft round suggestions

## Troubleshooting

### If Claude doesn't use MCP data:
- **Check server**: Is `python app/server.py` running?
- **Restart Claude**: Close and reopen Claude Desktop
- **Check connection**: Ask "What tools do you have access to?"

### If you get errors:
- **Server logs**: Check the terminal where you ran `python app/server.py`
- **Cache issues**: The server logs will show cache hits/misses
- **Network issues**: Ensure your internet connection is stable

## Ready to Draft!

Once setup is complete, you can ask questions like:

- "Should I draft [Player Name]?"
- "What's the best strategy from pick [X]?"
- "Who are the top [Position] available?"
- "Should I stack [QB] with [WR]?"

The assistant will use your MCP server data and provide PPR-specific analysis!
