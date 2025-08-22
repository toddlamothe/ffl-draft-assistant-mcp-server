# Fantasy Football Draft Assistant Configuration

This folder contains the system prompts and configuration files for using Claude Desktop as a Fantasy Football Draft Assistant with your MCP server.

## Files Overview

### 1. `fantasy_football_draft_assistant_prompt.md`
**Main system prompt** for Claude Desktop. This is the primary prompt you'll use during your draft.

**Key Features:**
- Comprehensive player analysis framework
- PPR-specific scoring considerations
- MCP server integration instructions
- Structured response format
- Draft strategy guidelines

### 2. `mcp_tools_reference.md`
**Quick reference guide** for the MCP server tools. This helps Claude understand how to use your data sources effectively.

**Key Features:**
- Tool descriptions and parameters
- Response format examples
- Usage strategies
- Integration tips

### 3. `sample_analysis_template.md`
**Example analyses** showing how the prompt works in practice. This demonstrates the expected output format.

**Key Features:**
- Sample player analyses (McCaffrey, Hill)
- Complete analysis structure
- PPR-specific insights
- Draft recommendations

## How to Use

### Setup in Claude Desktop

1. **Copy the main prompt**: Copy the contents of `fantasy_football_draft_assistant_prompt.md`

2. **Paste into Claude Desktop**: 
   - Open Claude Desktop
   - Go to Settings → Custom Instructions
   - Paste the prompt into the system prompt field

3. **Connect your MCP server**:
   - Ensure your MCP server is running (`python app/server.py`)
   - Claude Desktop should automatically detect and connect to your server

### During Your Draft

1. **Ask for player analysis**: 
   ```
   "Should I draft Christian McCaffrey?"
   "What round should I take Tyreek Hill?"
   "Is Austin Ekeler a good value in round 2?"
   ```

2. **Ask for position analysis**:
   ```
   "Who are the best RBs available in round 3?"
   "Should I go WR heavy early?"
   "What QBs should I target in the middle rounds?"
   ```

3. **Ask for strategic advice**:
   ```
   "I'm in round 5, what position should I target?"
   "Should I stack my QB with his WR1?"
   "What's my best strategy from the 8th pick?"
   ```

## Expected Output Format

Claude will provide structured analyses like this:

```
## Quick Take
[Player] is a [value assessment] in PPR leagues. [Brief reasoning].

## Detailed Analysis
[Comprehensive analysis using the framework]

## Draft Recommendation
**Round X-Y** | **Recommendation**: [Draft/Avoid/Consider]
**Reasoning**: [Clear explanation]

## Alternative Options
If [Player] is gone, consider: [List alternatives]
```

## Key Features

### PPR-Specific Analysis
- Prioritizes players with high reception potential
- Values pass-catching RBs higher than standard leagues
- Considers target share and offensive schemes
- Factors in reception volume for all positions

### MCP Server Integration
- Uses your player ratings data first
- Checks injury reports for QB/OL issues
- Analyzes team contexts and offensive schemes
- Provides data-driven recommendations

### Strategic Focus
- Round-specific value assessments
- Position scarcity considerations
- Team stacking opportunities
- Risk/reward analysis

## Tips for Best Results

1. **Be specific**: Ask about specific players, rounds, or situations
2. **Provide context**: Mention your draft position, league size, or current team needs
3. **Ask follow-ups**: Request clarification on recommendations
4. **Use the tools**: Claude will automatically use your MCP server data

## Example Questions

### Player Analysis
- "Should I draft Christian McCaffrey at pick 3?"
- "What's the value on Tyreek Hill in round 2?"
- "Is Bijan Robinson worth a first-round pick?"

### Position Strategy
- "Should I go RB heavy early?"
- "What's the best WR strategy in PPR?"
- "When should I draft my QB?"

### Draft Strategy
- "I'm picking 8th, what's my best strategy?"
- "Should I stack my QB with his WR1?"
- "What positions should I target in rounds 5-8?"

## Troubleshooting

### If Claude isn't using MCP data:
- Ensure your MCP server is running
- Check that Claude Desktop is connected to your server
- Ask Claude to explicitly use the MCP tools

### If responses are too generic:
- Ask for specific round recommendations
- Request PPR-specific analysis
- Ask for alternative options

### If you need more detail:
- Ask for injury analysis
- Request team context
- Ask for position-specific insights

## Customization

You can customize the prompt by:
- Adjusting the analysis framework
- Adding specific league rules
- Modifying the response format
- Including additional data sources

Remember: The goal is to provide strategic, data-driven advice that helps you win your PPR fantasy football league!
