const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
require('dotenv').config();

const app = express();

app.use(bodyParser.json());
app.use(cookieParser());

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

// User Schema and Model
const UserSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

UserSchema.pre('save', async function (next) {
    if (!this.isModified('password')) {
        return next();
    }
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
});

UserSchema.methods.comparePassword = function (candidatePassword) {
    return bcrypt.compare(candidatePassword, this.password);
};

const User = mongoose.model('User', UserSchema);

// Custom Model Schema and Model
const CustomModelSchema = new mongoose.Schema({
    name: { type: String, required: true },
    description: { type: String, required: true },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true }
});

const CustomModel = mongoose.model('CustomModel', CustomModelSchema);

// Middleware for authentication
const auth = async (req, res, next) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(401).send('Access Denied');
    }
    try {
        const verified = jwt.verify(token, process.env.JWT_SECRET);
        req.user = await User.findById(verified.id);
        next();
    } catch (err) {
        res.status(400).send('Invalid Token');
    }
};

// Auth Routes
app.post('/auth/signup', async (req, res) => {
    try {
        const { username, password } = req.body;
        const newUser = new User({ username, password });
        await newUser.save();
        res.status(201).send('User created');
    } catch (err) {
        res.status(400).send(err.message);
    }
});

app.post('/auth/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        const user = await User.findOne({ username });
        if (!user || !(await user.comparePassword(password))) {
            return res.status(400).send('Invalid credentials');
        }
        const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
        res.cookie('token', token, { httpOnly: true });
        res.send('Logged in');
    } catch (err) {
        res.status(400).send(err.message);
    }
});

app.post('/auth/logout', (req, res) => {
    res.clearCookie('token');
    res.send('Logged out');
});

// Custom Model Routes
app.post('/customModel/create', auth, async (req, res) => {
    try {
        const { name, description } = req.body;
        const newModel = new CustomModel({ name, description, userId: req.user._id });
        await newModel.save();
        res.status(201).send('Custom model created');
    } catch (err) {
        res.status(400).send(err.message);
    }
});

app.get('/customModel', auth, async (req, res) => {
    try {
        const models = await CustomModel.find({ userId: req.user._id });
        res.json(models);
    } catch (err) {
        res.status(400).send(err.message);
    }
});

app.get('/customModel/:id', auth, async (req, res) => {
    try {
        const model = await CustomModel.findById(req.params.id);
        if (!model || model.userId.toString() !== req.user._id.toString()) {
            return res.status(404).send('Model not found');
        }
        res.json(model);
    } catch (err) {
        res.status(400).send(err.message);
    }
});

app.delete('/customModel/:id', auth, async (req, res) => {
    try {
        const model = await CustomModel.findById(req.params.id);
        if (!model || model.userId.toString() !== req.user._id.toString()) {
            return res.status(404).send('Model not found');
        }
        await model.remove();
        res.send('Model deleted');
    } catch (err) {
        res.status(400).send(err.message);
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
