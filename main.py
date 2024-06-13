import os
import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import chromadb
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.img_utils import _to_pil, get_image_data
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.code_utils import DEFAULT_MODEL, UNKNOWN, content_str, execute_code, extract_code, infer_lang

# Debugging: Check current working directory and list files
print("Current Working Directory:", os.getcwd())
print("Files in Directory:", os.listdir())

# Assuming the file is in the same directory, provide a relative path
config_file_path = "OAI_CONFIG_LIST.json"  # or provide the correct path

# Ensure the file exists
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

# Load configuration
config_list_gemini = autogen.config_list_from_json(
    config_file_path,
    filter_dict={
        "model": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-pro-001"],
    },
)

config_list_gemini_vision = autogen.config_list_from_json(
    config_file_path,
    filter_dict={
        "model": ["gemini-pro-vision"],
    },
)

seed = 25  # for caching

coder = AssistantAgent(
    name="Coder",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at writing code",
)

pm = AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at designing products and software.",
)

scientist = AssistantAgent(
    name="Scientist",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at scientific research and analysis.",
)

doctor = AssistantAgent(
    name="Doctor",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at providing medical advice and diagnosis.",
)

sportsman = AssistantAgent(
    name="Sportsman",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at sports and physical fitness.",
)

artist = AssistantAgent(
    name="Artist",
    llm_config={"config_list": config_list_gemini, "seed": seed},
    max_consecutive_auto_reply=10,
    description="I am good at creating art and design.",
)

user_proxy = UserProxyAgent(
    name="User_proxy",
    code_execution_config={"last_n_messages": 20, "work_dir": "coding", "use_docker": False},
    human_input_mode="NEVER",
    is_termination_msg=lambda x: content_str(x.get("content")).find("TERMINATE") >= 0,
    description="I stand for the user and can run code.",
)

agents = {
    "coder": coder,
    "product_manager": pm,
    "scientist": scientist,
    "doctor": doctor,
    "sportsman": sportsman,
    "artist": artist,
}

def initiate_single_chat(agent_name: str, message: str):
    if agent_name not in agents:
        raise ValueError(f"Unknown agent name: {agent_name}")
    
    agent = agents[agent_name]
    
    groupchat = autogen.GroupChat(agents=[user_proxy, agent], messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list_gemini, "seed": seed},
        is_termination_msg=lambda x: content_str(x.get("content")).find("TERMINATE") >= 0,
    )
    
    user_proxy.initiate_chat(manager, message=message)

def initiate_group_chat(agent_names: List[str], message: str):
    selected_agents = [user_proxy]
    
    for name in agent_names:
        if name not in agents:
            raise ValueError(f"Unknown agent name: {name}")
        selected_agents.append(agents[name])
    
    groupchat = autogen.GroupChat(agents=selected_agents, messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list_gemini, "seed": seed},
        is_termination_msg=lambda x: content_str(x.get("content")).find("TERMINATE") >= 0,
    )
    
    user_proxy.initiate_chat(manager, message=message)
