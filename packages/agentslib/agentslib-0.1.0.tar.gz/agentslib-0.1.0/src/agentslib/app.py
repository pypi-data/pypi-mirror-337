from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from .tools import FinalAnswerTool

from .ui.Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

# model = HfApiModel(
# max_tokens=2096,
# temperature=0.5,
# model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
# custom_role_conversions=None,
# )

import os
from smolagents import OpenAIServerModel

model = OpenAIServerModel(
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    api_base="http://localhost:8000/v1",
    api_key="asd",
)

# Import tool from Hub
# image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
search_agent = CodeAgent(
    name='search_agent',
    model=model,
    tools=[final_answer, get_current_time_in_timezone, DuckDuckGoSearchTool()], ## add your tools here (don't remove final answer)
    max_steps=20,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    description=None,
    prompt_templates=prompt_templates,
    additional_authorized_imports=['requests', 'bs4', 'gradio', 'numpy', 'numpy.random', 'numpy.linalg',
                                   'scikit-learn', 'sklearn', # for sklearn
                                   'matplotlib', 'pandas', 'seaborn', 'pytz', 'scipy'],
)


GradioUI(search_agent).launch()