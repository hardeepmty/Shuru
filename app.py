import os
import json
from flask import Flask, request, jsonify
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from typing import List

app = Flask(__name__)

# Configuration file path
CONFIG_FILE_PATH = "OAI_CONFIG_LIST.json"

# Load configuration list from a JSON file
def load_config_list(config_file_path):
    return autogen.config_list_from_json(config_file_path)

# Create an AssistantAgent model based on user input for name and description
def create_model(name, description):
    config_list = load_config_list(CONFIG_FILE_PATH)  # Replace with actual path
    seed = 42  # Seed value for consistency

    return autogen.AssistantAgent(
        name=name,
        llm_config={
            "config_list": config_list,
            "seed": seed,
        },
        max_consecutive_auto_reply=10,
        description=description,
    )

# Initiate a single chat interaction with the selected agent
def initiate_single_chat(agent, message):
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        code_execution_config={"last_n_messages": 20, "work_dir": "coding", "use_docker": False},
        human_input_mode="NEVER",
        is_termination_msg=lambda x: autogen.code_utils.content_str(x.get("content")).find("TERMINATE") >= 0,
        description="I stand for the user and can run code.",
    )

    groupchat = autogen.GroupChat(agents=[user_proxy, agent], messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=agent.llm_config,
        is_termination_msg=lambda x: autogen.code_utils.content_str(x.get("content")).find("TERMINATE") >= 0,
    )
    
    user_proxy.initiate_chat(manager, message=message)
    responses = []
    for msg in groupchat.messages:
        responses.append(msg["content"])
    return responses

# Initiate a group chat interaction with the selected agents
def initiate_group_chat(agents, message):
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        code_execution_config={"last_n_messages": 20, "work_dir": "coding", "use_docker": False},
        human_input_mode="NEVER",
        is_termination_msg=lambda x: autogen.code_utils.content_str(x.get("content")).find("TERMINATE") >= 0,
        description="I stand for the user and can run code.",
    )

    groupchat = autogen.GroupChat(agents=[user_proxy] + agents, messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=agents[0].llm_config,  # Assuming all agents have the same llm_config
        is_termination_msg=lambda x: autogen.code_utils.content_str(x.get("content")).find("TERMINATE") >= 0,
    )
    
    user_proxy.initiate_chat(manager, message=message)
    responses = []
    for msg in groupchat.messages:
        responses.append(msg["content"])
    return responses

# Predefined agents
agents = {
    "coder": AssistantAgent(
        name="Coder",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at writing code",
    ),
    "product_manager": AssistantAgent(
        name="Product_manager",
        system_message="Creative in software product ideas.",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at designing products and software.",
    ),
    "scientist": AssistantAgent(
        name="Scientist",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at scientific research and analysis.",
    ),
    "doctor": AssistantAgent(
        name="Doctor",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at providing medical advice and diagnosis.",
    ),
    "sportsman": AssistantAgent(
        name="Sportsman",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at sports and physical fitness.",
    ),
    "artist": AssistantAgent(
        name="Artist",
        llm_config={"config_list": load_config_list(CONFIG_FILE_PATH), "seed": 42},
        max_consecutive_auto_reply=10,
        description="I am good at creating art and design.",
    ),
}

custom_models = []

@app.route("/create_model", methods=["POST"])
def api_create_model():
    data = request.json
    model_name = data.get("name")
    model_description = data.get("description")

    custom_model = create_model(model_name, model_description)
    custom_models.append(custom_model)
    return jsonify({"message": f"Custom model '{model_name}' created successfully!"})

@app.route("/single_chat", methods=["POST"])
def api_single_chat():
    data = request.json
    model_name = data.get("model_name")
    message = data.get("message")

    agent = agents.get(model_name) or next((m for m in custom_models if m.name == model_name), None)
    if not agent:
        return jsonify({"error": "Model not found"}), 404

    try:
        responses = initiate_single_chat(agent, message)
        return jsonify({"responses": responses})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/group_chat", methods=["POST"])
def api_group_chat():
    data = request.json
    model_names = data.get("model_names")
    message = data.get("message")

    selected_agents = [agents.get(name) or next((m for m in custom_models if m.name == name), None) for name in model_names]
    selected_agents = [agent for agent in selected_agents if agent]

    if len(selected_agents) < 2:
        return jsonify({"error": "You need to select at least two valid models for a group chat"}), 400

    try:
        responses = initiate_group_chat(selected_agents, message)
        return jsonify({"responses": responses})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
