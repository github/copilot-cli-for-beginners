// userService.js - Sample code with intentional bugs for practice
// Use this file to practice code review and debugging with GitHub Copilot CLI
//
// Try these commands:
//   copilot --allow-all -p "Review @samples/buggy-code/js/userService.js for security issues"
//   copilot --allow-all -p "Find all bugs in @samples/buggy-code/js/userService.js"

const db = require('./db');

// BUG 1: SQL Injection
// The userId is directly concatenated into the query string
async function getUser(userId) {
  return db.query(`SELECT * FROM users WHERE id = ${userId}`);
}

// BUG 2: Race Condition
// Multiple requests can trigger parallel database calls before cache is set
let userCache = {};
async function getCachedUser(userId) {
  if (!userCache[userId]) {
    userCache[userId] = await getUser(userId);
  }
  return userCache[userId];
}

// BUG 3: SQL Injection + No Error Handling
// String interpolation in SQL and no try/catch
async function updateUser(userId, data) {
  await db.query(`UPDATE users SET name = '${data.name}' WHERE id = ${userId}`);
  return getUser(userId);
}

// BUG 4: Sensitive Data in Logs
// Password is logged in plain text
async function login(email, password) {
  console.log(`Login attempt: ${email} / ${password}`);
  const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);
  if (user.password === password) {
    return { success: true, user };
  }
  return { success: false };
}

// BUG 5: Weak Password Comparison
// Using == instead of === and comparing plain text passwords
async function verifyPassword(inputPassword, storedPassword) {
  return inputPassword == storedPassword;
}

// BUG 6: No Input Validation
// Directly using user input without any validation
async function createUser(userData) {
  const query = `INSERT INTO users (name, email, password) VALUES ('${userData.name}', '${userData.email}', '${userData.password}')`;
  return db.query(query);
}

// BUG 7: Hardcoded Secret
// JWT secret should be in environment variables
const JWT_SECRET = 'super-secret-key-12345';

function generateToken(userId) {
  return jwt.sign({ userId }, JWT_SECRET);
}

// BUG 8: Missing Authentication Check
// This endpoint should verify the user is authorized
async function deleteUser(userId) {
  return db.query(`DELETE FROM users WHERE id = ${userId}`);
}

module.exports = {
  getUser,
  getCachedUser,
  updateUser,
  login,
  verifyPassword,
  createUser,
  generateToken,
  deleteUser
};
