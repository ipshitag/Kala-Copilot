from azure.ai.projects.models import FunctionTool, ToolSet, MessageTextContent
from agent_tools import (
    image_describing_tool,
    campaign_generation_tool
)

visual_insight_functions_tool = FunctionTool(
    {
        image_describing_tool
    }
)
visual_insight_functions_toolset = ToolSet()
visual_insight_functions_toolset.add(visual_insight_functions_tool)