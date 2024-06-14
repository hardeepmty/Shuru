import requests

BASE_URL = 'http://localhost:3000'
LOGIN_ENDPOINT = '/auth/login'
LOGOUT_ENDPOINT = '/auth/logout'
SIGNUP_ENDPOINT = '/auth/signup'
MODEL_ENDPOINT = '/customModel'

session = requests.Session()

def signup(username, password):
    response = session.post(BASE_URL + SIGNUP_ENDPOINT, json={'username': username, 'password': password})
    print(response.text)

def login(username, password):
    response = session.post(BASE_URL + LOGIN_ENDPOINT, json={'username': username, 'password': password})
    print(response.text)

def logout():
    response = session.post(BASE_URL + LOGOUT_ENDPOINT)
    print(response.text)

def create_model(name, description):
    response = session.post(BASE_URL + MODEL_ENDPOINT + '/create', json={'name': name, 'description': description})
    print(response.text)

def get_models():
    response = session.get(BASE_URL + MODEL_ENDPOINT)
    print(response.json())

def get_model(model_id):
    response = session.get(BASE_URL + MODEL_ENDPOINT + f'/{model_id}')
    print(response.json())

def delete_model(model_id):
    response = session.delete(BASE_URL + MODEL_ENDPOINT + f'/{model_id}')
    print(response.text)

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Signup")
        print("2. Login")
        print("3. Logout")
        print("4. Create Model")
        print("5. Get Models")
        print("6. Get Model")
        print("7. Delete Model")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            signup(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == '3':
            logout()
        elif choice == '4':
            name = input("Enter model name: ")
            description = input("Enter model description: ")
            create_model(name, description)
        elif choice == '5':
            get_models()
        elif choice == '6':
            model_id = input("Enter model ID: ")
            get_model(model_id)
        elif choice == '7':
            model_id = input("Enter model ID: ")
            delete_model(model_id)
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

if __name__ == "__main__":
    print("Welcome to Model Interaction!")
    main_menu()
