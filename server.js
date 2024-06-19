const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 3000;

app.use(bodyParser.json());

const predefinedModels = {
    "coder": {
        name: "Coder",
        description: "I am good at writing code"
    },
    "artist": {
        name: "Artist",
        description: "I am good at creating art and design."
    },
    "doctor": {
        name: "Doctor",
        description: "I am good at providing medical advice and diagnosis."
    },
    "scientist": {
        name: "Scientist",
        description: "I am good at scientific research and analysis."
    },
    "sportsman": {
        name: "Sportsman",
        description: "I am good at sports and physical fitness."
    },
    "product_manager": {
        name: "Product Manager",
        description: "I am good at designing products and software."
    }
};

let customModels = [];

// Route to get all predefined models
app.get('/api/predefined-models', (req, res) => {
    res.json(Object.values(predefinedModels));
});

// Route to create a custom model
app.post('/api/custom-model', async (req, res) => {
    const { name, description } = req.body;
    const newModel = { name, description };

    try {
        // Make a request to the Flask server to create the custom model
        await axios.post('http://localhost:5000/custom-model', newModel);
        customModels.push(newModel);
        res.json(newModel);
    } catch (error) {
        console.error("Error creating custom model:", error);
        res.status(500).json({ error: "Failed to create custom model" });
    }
});

// Route to initiate a single chat with a model
app.post('/api/chat/:model', async (req, res) => {
    const { model } = req.params;
    const { message } = req.body;

    // Check if the model is predefined
    if (predefinedModels[model]) {
        try {
            const response = await simulateChat(predefinedModels[model], message);
            res.json({ response });
        } catch (error) {
            res.status(500).json({ error: "Failed to get response from the model" });
        }
    } else {
        // Check if the model is custom
        const customModel = customModels.find(m => m.name === model);
        if (customModel) {
            try {
                const response = await simulateChat(customModel, message);
                res.json({ response });
            } catch (error) {
                res.status(500).json({ error: "Failed to get response from the model" });
            }
        } else {
            res.status(404).json({ error: "Model not found" });
        }
    }
});

// Route to initiate a group chat with multiple models
app.post('/api/group-chat', async (req, res) => {
    const { modelNames, message } = req.body;
    const selectedModels = [];

    // Check predefined models
    modelNames.forEach(name => {
        if (predefinedModels[name]) {
            selectedModels.push(predefinedModels[name]);
        }
    });

    // Check custom models
    modelNames.forEach(name => {
        const customModel = customModels.find(m => m.name === name);
        if (customModel) {
            selectedModels.push(customModel);
        }
    });

    if (selectedModels.length === 0) {
        res.status(404).json({ error: "No valid models found" });
    } else {
        try {
            const responses = await Promise.all(
                selectedModels.map(model => simulateChat(model, message))
            );
            res.json({ responses });
        } catch (error) {
            res.status(500).json({ error: "Failed to get responses from the models" });
        }
    }
});

// Function to simulate chat interaction by calling the Flask server
const simulateChat = async (model, message) => {
    try {
        const response = await axios.post(`http://localhost:5000/chat/${model.name.toLowerCase()}`, { message });
        return response.data.response;
    } catch (error) {
        console.error(`Error interacting with model ${model.name}:`, error);
        throw error;
    }
};

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
