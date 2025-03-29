from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional
from .analyzer import preprocess_input, analyze_user_story, format_invest_results

# Initialize MCP server
mcp = FastMCP("userstory-invest-mcp")

@mcp.tool(description="Analyzes user stories using the INVEST criteria and suggests improvements.")
async def invest_analyze(
    user_story: Dict[str, Any],
    format_output: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Analyze a user story using INVEST criteria and provide improvement recommendations.
    
    Parameters:
    user_story (Dict): A user story object containing at minimum Title, Description, and AcceptanceCriteria
    format_output (bool): Whether to return the results as formatted text (True) or raw JSON (False)
    
    Returns:
    Dict: Analysis results with INVEST scores and improvement suggestions
    """
    try:
        # Preprocess the input to handle various formats
        processed_story = preprocess_input(user_story)
        
        # Perform the INVEST analysis
        analysis_result = analyze_user_story(processed_story)
        
        if format_output:
            # Return a formatted text version for human readability
            formatted_results = format_invest_results(analysis_result)
            return {"content": [{"type": "text", "text": formatted_results}]}
        else:
            # Return the raw analysis results as JSON
            return {"content": [{"type": "json", "json": analysis_result}]}
            
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error analyzing user story: {str(e)}"}], "isError": True}

if __name__ == "__main__":
    print("UserStory INVEST Analyzer MCP server running on stdio...")
    mcp.run()