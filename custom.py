import autogen

def load_config_list(config_file_path):
    """
    Load configuration list from a JSON file.
    """
    return autogen.config_list_from_json(config_file_path)

def create_model(name, description):
    """
    Create an AssistantAgent model based on user input for name and description.
    """
    config_list = load_config_list("OAI_CONFIG_LIST.json")  # Replace with actual path
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

def initiate_single_chat(agent: autogen.AssistantAgent, message: str):
    """
    Initiate a single chat interaction with the selected agent.
    """
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

if __name__ == "__main__":
    print("Welcome to Model Interaction!")
    print("You can now interact with different models.")
    
    # Prompt user to define the model
    model_name = input("Enter the name for your custom model: ")
    model_description = input("Enter a brief description for your custom model: ")

    # Create the custom model
    custom_model = create_model(model_name, model_description)
    print(f"\nInteracting with {custom_model.name}: {custom_model.description}")

    while True:
        message = input("You: ")

        if message.lower() == 'exit':
            print("Exiting...")
            break

        try:
            initiate_single_chat(custom_model, message)
        except autogen.generativeai.types.generation_types.StopCandidateException as e:
            print("The response was flagged for potential harmful content. Please try again with a different message.")
        except Exception as e:
            print(f"An error occurred: {e}")
