from flask import Flask, request, jsonify

app = Flask(__name__)

predefined_models = {
    'coder': {'name': 'Coder', 'description': 'I am good at writing code'},
    'artist': {'name': 'Artist', 'description': 'I am good at creating art and design.'},
    'doctor': {'name': 'Doctor', 'description': 'I am good at providing medical advice and diagnosis.'},
    'scientist': {'name': 'Scientist', 'description': 'I am good at scientific research and analysis.'},
    'sportsman': {'name': 'Sportsman', 'description': 'I am good at sports and physical fitness.'},
    'product_manager': {'name': 'Product Manager', 'description': 'I am good at designing products and software.'}
}

custom_models = []

@app.route('/predefined-models', methods=['GET'])
def get_predefined_models():
    return jsonify(list(predefined_models.values()))

@app.route('/custom-model', methods=['POST'])
def create_custom_model():
    data = request.json
    custom_models.append(data)
    return jsonify(data)

@app.route('/chat/<model>', methods=['POST'])
def chat_with_model(model):
    data = request.json
    message = data['message']
    if model in predefined_models:
        response = f"Response from {predefined_models[model]['name']}: This is a simulated response to your message '{message}'"
    else:
        custom_model = next((m for m in custom_models if m['name'] == model), None)
        if custom_model:
            response = f"Response from {custom_model['name']}: This is a simulated response to your message '{message}'"
        else:
            return jsonify({'error': 'Model not found'}), 404
    return jsonify({'response': response})

@app.route('/group-chat', methods=['POST'])
def group_chat():
    data = request.json
    model_names = data['modelNames']
    message = data['message']
    responses = []
    for model_name in model_names:
        if model_name in predefined_models:
            responses.append(f"Response from {predefined_models[model_name]['name']}: This is a simulated response to your message '{message}'")
        else:
            custom_model = next((m for m in custom_models if m['name'] == model_name), None)
            if custom_model:
                responses.append(f"Response from {custom_model['name']}: This is a simulated response to your message '{message}'")
    if not responses:
        return jsonify({'error': 'No valid models found'}), 404
    return jsonify({'responses': responses})

if __name__ == '__main__':
    app.run(port=5000)
