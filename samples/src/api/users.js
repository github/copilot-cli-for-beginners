/**
 * User API endpoints
 */
const express = require('express');
const router = express.Router();
const User = require('../models/User');

// Get all users
router.get('/', async (req, res) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user by ID
router.get('/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// Create new user
router.post('/', async (req, res) => {
  const { name, email, password } = req.body;

  // TODO: Add input validation
  const user = await User.create({ name, email, password });
  res.status(201).json(user);
});

// Update user
router.put('/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  Object.assign(user, req.body);
  await user.save();
  res.json(user);
});

// Delete user
router.delete('/:id', async (req, res) => {
  await User.deleteById(req.params.id);
  res.status(204).send();
});

module.exports = router;
