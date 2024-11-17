
import json

from downedit.agents.invoker import invoke_tool
from downedit.agents.prompts import build_main_prompt
from downedit.utils import (
    log
)

# class DownEditAgent:

#     def __init__(self, llm):
#         self.llm = llm
#         self.main_prompt = build_main_prompt()


#     async def process_request(self, user_request: str):
#         """
#         Processes a user request and executes tools.
#         """

#         prompt = f"{self.main_prompt}\nUser Request:\n{user_request}"
#         llm_response = self.llm(prompt)

#         tool_name, tool_args = self.parse_llm_response(llm_response)

#         if tool_name and tool_args:
#             try:
#                 tool_result = await invoke_tool(tool_name, tool_args)
#                 final_response = f"Tool '{tool_name}' executed successfully.\nResult:\n{tool_result}"

#             except ValueError as e:
#                 final_response = f"Invalid tool or arguments: {e}"
#             except Exception as e:
#                 final_response = f"Error executing tool: {e}"
#         else:
#             final_response = "I could not understand your request or determine the correct tool to use.  Please rephrase or provide more details."

#         return final_response

#     def parse_llm_response(self, llm_response):
#         """
#         Parses the LLM response to extract the tool and its arguments.
#         This is highly dependent on how your LLM returns function calls.
#         """

#         try:
#             response_json = json.loads(llm_response)
#             tool_name = response_json["tool_name"]
#             tool_args = response_json["tool_args"]

#         except (json.JSONDecodeError, KeyError) as e:
#             log.error(f"Could not parse LLM response: {e}")
#             return None, None
#         return tool_name, tool_args