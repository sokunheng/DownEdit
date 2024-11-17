MAIN_PROMPT = """
You are an AI assistant designed to deliver precise, context-specific responses to user inquiries with Python code that will perform the task.
Your responses should rely exclusively on the details and descriptors explicitly provided within the given context.
To support your task, you are equipped with a set of tools. Each tool is a Python function with a clear description of its purpose, expected inputs, and outputs.
Use these tools effectively to enhance the accuracy and relevance of your responses.
In situations where the available information is insufficient to provide a definitive answer or perform a requested action, respond clearly with "I don't know." or "I cannot do that."
Feel free to print intermediate results when it helps to clarify or verify the process. Always prioritize clarity, accuracy, and user satisfaction in your interactions.
"""

PROMPTS = {
    "edit_video": {
        "description": "Edits videos with various operations like flipping, changing speed, adding music, looping, and adjusting color.",
        "parameters": {
            "tool": {
                "type": "string",
                "description": "The name of the video editing tool to use. Options: Flip Horizontal, Custom Speed, Loop Video, Flip + Speed, Add Music, Speed + Music, Flip + Speed + Music, Adjust Color"
            },
            "process_folder": {
                "type": "string",
                "description": "The path to the folder containing the video files to process."
            },
            "batch_size": {
                "type": "integer",
                "description": "The number of videos to process in each batch (default: 5, max 10)."
            },
            "speed": {
                "type": "float",
                "description": "Speed factor for video processing."
            },
            "music": {
                "type": "string",
                "description": "Path to music file to add to the video."
            },
            "threads": {
                "type": "integer",
                "description": "Number of CPU threads to use for video processing."
            },
            "preset": {
                "type": "string",
                "description": "Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow)."
            }
        },
        "examples": [
            {
                "input": "Flip all videos in the folder /path/to/videos horizontally.",
                "output": """
                ```json
                {
                    "tool_name": "edit_video",
                    "tool_args": {
                        "tool": "Flip Horizontal",
                        "process_folder": "/path/to/videos",
                        "batch_size": 5,
                        "threads": 1,
                        "preset": "medium"
                    }
                }
                ```
                """
            },
            {
                "input": "Speed up videos in /path/to/videos 2x, using 4 threads and the ultrafast preset.",
                "output": """
                ```json
                {
                    "tool_name": "edit_video",
                    "tool_args": {
                        "tool": "Custom Speed",
                        "process_folder": "/path/to/videos",
                        "batch_size": 5,
                        "speed": 2.0,
                        "threads": 4,
                        "preset": "ultrafast"
                    }
                }
                ```
                """
            }
        ]
    },
    "edit_image": {
        "description": "Edits images with various operations like flipping, cropping, rotating, and adjusting color.",
        "parameters": {
            "tool": {
                "type": "string",
                "description": "Image editing tool... (Options: Flip Horizontal, Crop Image, Rotate Image, Adjust Color)"
            },
            "process_folder": {
                "type": "string",
                "description": "Path to image folder to process..."
            },
            "batch_size": {
                "type": "integer",
                "description": "Batch size... (default: 5, max 10)"
            },
            "**image_params": {
                "type": "various",
                "description": "Additional parameters specific to the image editing tool."
            },
        },
        "examples": [
            {
                "input": "Rotate the images in C:/images 90 degrees clockwise.",
                "output": """
                ```json
                {
                    "tool_name": "edit_image",
                    "tool_args": {
                        "tool": "Rotate Image",
                        "process_folder": "C:/images",
                        "batch_size": 5,
                        "degrees": 90
                    }
                }
                ```
                """
            }
        ]
    },
    "edit_sound": {
        "description": "Edits sound files with various operations like adjusting volume, fading in/out.",
        "parameters": {
            "tool": {
                "type": "string",
                "description": "sound editing tool... (Options: Volume, Fade In, Fade Out)"
            },
            "process_folder": {
                "type": "string",
                "description": "Path to sound folder to process..."
            },
            "batch_size": {
                "type": "integer",
                "description": "Batch size... (default: 5, max 10)"
            },
            "level": {
                "type": "float",
                "description": "Volume level"
            },
        }
    },
    "generate_ai_image": {
        "description": "Generates AI images based on text prompts.",
        "parameters": {
            "prompt": {
                "type": "string",
                "description": "Text prompt for image generation..."
            },
            "size": {
                "type": "string",
                "description": "Image size (e.g., 512x512, 512x768, 768x512)",
            }
        },
    }
}


def get_tool_prompt(tool_name: str) -> str:
    """
    Retrieves the prompt for a specific tool.

    Args:
        tool_name (str): The name of the tool to retrieve the prompt for.
    """
    tool_data = PROMPTS.get(tool_name)
    tool_prompt = f"{tool_name}:\n{tool_data['description']}\nParameters:\n"

    for param_name, param_data in tool_data["parameters"].items():
            tool_prompt += f"- {param_name}: {param_data['description']} (type: {param_data['type']})\n"

    if tool_data.get("examples"):
            tool_prompt += "\nExamples:\n"
            for example in tool_data["examples"]:
                tool_prompt += f"Input: {example['input']}\nOutput:\n{example['output']}\n"

    return tool_prompt

def build_main_prompt() -> str:
    """
    Builds the main prompt with tool descriptions.
    """
    main_prompt = MAIN_PROMPT
    for tool_name in PROMPTS:
        main_prompt += get_tool_prompt(tool_name) + "\n"
    return main_prompt
