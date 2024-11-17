import asyncio

from downedit.agents.registry import get_tool


async def invoke_tool(tool_name: str, tool_args: dict):
    """
    Invokes the specified tool with the given arguments.

    Args:
        tool_name (str): The name of the tool to invoke.
        tool_args (dict): The arguments to pass to the tool.
    """
    tool_class = get_tool(tool_name)
    if not tool_class:
        raise ValueError(f"Invalid tool name: {tool_name}")

    try:
        with tool_class(**tool_args) as tool_instance:
            if asyncio.iscoroutinefunction(tool_instance.start):
                result = await tool_instance.start()
            else:
                result = tool_instance.start()
        return result
    except Exception as e:
        return f"Error invoking tool: {e}"