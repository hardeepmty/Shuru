import custom
import customMulti
import main
import autogen

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Custom Single Model Interaction")
        print("2. Custom Multi-Model Interaction")
        print("3. Predefined Model Interaction")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            custom_model_interaction()
        elif choice == '2':
            custom_multi_model_interaction()
        elif choice == '3':
            predefined_model_interaction()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

def custom_model_interaction():
    model_name = input("Enter the name for your custom model: ")
    model_description = input("Enter a brief description for your custom model: ")

    custom_model = custom.create_model(model_name, model_description)
    print(f"\nInteracting with {custom_model.name}: {custom_model.description}")

    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            print("Exiting...")
            break
        try:
            custom.initiate_single_chat(custom_model, message)
        except autogen.generativeai.types.generation_types.StopCandidateException as e:
            print("The response was flagged for potential harmful content. Please try again with a different message.")
        except Exception as e:
            print(f"An error occurred: {e}")

def custom_multi_model_interaction():
    custom_models = []

    while True:
        print("\nCustom Multi-Model Menu:")
        print("1. Create a new custom model")
        print("2. Start a single chat with a model")
        print("3. Start a group chat with multiple models")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            model_name = input("Enter the name for your custom model: ")
            model_description = input("Enter a brief description for your custom model: ")
            custom_model = customMulti.create_model(model_name, model_description)
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
                    customMulti.initiate_single_chat(custom_models[model_index], message)
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
                customMulti.initiate_group_chat(selected_models, message)
            except autogen.generativeai.types.generation_types.StopCandidateException as e:
                print("The response was flagged for potential harmful content. Please try again with a different message.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

def predefined_model_interaction():
    while True:
        print("\nPredefined Model Interaction Menu:")
        print("1. Start a single chat with a predefined model")
        print("2. Start a group chat with predefined models")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Available models:")
            for agent_name, agent in main.agents.items():
                print(f"- {agent_name.capitalize()}: {agent.description}")
            agent_name = input("Enter the name of the model to chat with: ").lower()
            message = input("You: ")
            try:
                main.initiate_single_chat(agent_name, message)
            except ValueError as e:
                print(e)
            except autogen.generativeai.types.generation_types.StopCandidateException as e:
                print("The response was flagged for potential harmful content. Please try again with a different message.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
            print("Available models:")
            for agent_name, agent in main.agents.items():
                print(f"- {agent_name.capitalize()}: {agent.description}")
            agent_names = input("Enter the names of the models to include in the group chat (comma-separated): ").lower().split(',')
            message = input("You: ")
            try:
                main.initiate_group_chat(agent_names, message)
            except ValueError as e:
                print(e)
            except autogen.generativeai.types.generation_types.StopCandidateException as e:
                print("The response was flagged for potential harmful content. Please try again with a different message.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    print("Welcome to Model Interaction!")
    main_menu()
