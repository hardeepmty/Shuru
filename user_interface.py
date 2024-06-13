import sys
from main import initiate_single_chat, initiate_group_chat

def select_single_or_group():
    print("Do you want to interact with a single model or a group chat?")
    print("1. Single Model")
    print("2. Group Chat")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        return "single"
    elif choice == "2":
        return "group"
    else:
        print("Invalid choice. Please select a valid option.")
        sys.exit(1)

def select_model():
    print("Select a model to interact with:")
    print("1. Coder")
    print("2. Product Manager")
    print("3. Scientist")
    print("4. Doctor")
    print("5. Sportsman")
    print("6. Artist")
    
    choice = input("Enter the number of the model: ")
    
    if choice == "1":
        return "coder"
    elif choice == "2":
        return "product_manager"
    elif choice == "3":
        return "scientist"
    elif choice == "4":
        return "doctor"
    elif choice == "5":
        return "sportsman"
    elif choice == "6":
        return "artist"
    else:
        print("Invalid choice. Please select a valid option.")
        sys.exit(1)

def select_multiple_models():
    print("Select models to interact with (separate choices with commas):")
    print("1. Coder")
    print("2. Product Manager")
    print("3. Scientist")
    print("4. Doctor")
    print("5. Sportsman")
    print("6. Artist")
    
    choices = input("Enter the numbers of the models: ").split(",")
    models = []
    
    for choice in choices:
        choice = choice.strip()
        if choice == "1":
            models.append("coder")
        elif choice == "2":
            models.append("product_manager")
        elif choice == "3":
            models.append("scientist")
        elif choice == "4":
            models.append("doctor")
        elif choice == "5":
            models.append("sportsman")
        elif choice == "6":
            models.append("artist")
        else:
            print(f"Invalid choice: {choice}. Please select a valid option.")
            sys.exit(1)
    
    return models

def main():
    interaction_type = select_single_or_group()
    
    if interaction_type == "single":
        agent_name = select_model()
        message = input("Enter the message you want to send: ")
        initiate_single_chat(agent_name, message)
    else:
        agent_names = select_multiple_models()
        message = input("Enter the message you want to send: ")
        initiate_group_chat(agent_names, message)

if __name__ == "__main__":
    main()
