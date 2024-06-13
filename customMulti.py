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

def initiate_group_chat(agents, message: str):
    """
    Initiate a group chat interaction with the selected agents.
    """
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

if __name__ == "__main__":
    print("Welcome to Model Interaction!")
    print("You can now interact with different models.")

    custom_models = []

    while True:
        print("\nOptions:")
        print("1. Create a new custom model")
        print("2. Start a single chat with a model")
        print("3. Start a group chat with multiple models")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            model_name = input("Enter the name for your custom model: ")
            model_description = input("Enter a brief description for your custom model: ")
            custom_model = create_model(model_name, model_description)
            custom_models.append(custom_model)
            print(f"Custom model '{model_name}' created successfully!")

        elif choice == '2':
            if not custom_models:
                print("No custom models available. Please create one first.")
                continue
            print("Available models:")
            for i, model in enumerate(custom_models):
                print(f"{i + 1}. {model.name} - {model.description}")
            model_index = int(input("Enter the number of the model to chat with: ")) - 1
            message = input("You: ")
            if 0 <= model_index < len(custom_models):
                try:
                    initiate_single_chat(custom_models[model_index], message)
                except autogen.generativeai.types.generation_types.StopCandidateException as e:
                    print("The response was flagged for potential harmful content. Please try again with a different message.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Invalid model number.")

        elif choice == '3':
            if len(custom_models) < 2:
                print("You need at least two models to start a group chat.")
                continue
            print("Available models:")
            for i, model in enumerate(custom_models):
                print(f"{i + 1}. {model.name} - {model.description}")
            model_indices = input("Enter the numbers of the models to include in the group chat (comma-separated): ").split(',')
            selected_models = [custom_models[int(index) - 1] for index in model_indices if index.isdigit() and 0 <= int(index) - 1 < len(custom_models)]
            if len(selected_models) < 2:
                print("You need to select at least two valid models for a group chat.")
                continue
            message = input("You: ")
            try:
                initiate_group_chat(selected_models, message)
            except autogen.generativeai.types.generation_types.StopCandidateException as e:
                print("The response was flagged for potential harmful content. Please try again with a different message.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
