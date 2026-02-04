/**
 * User service for business logic
 */

const userCache = {};

async function getUser(userId) {
  // Check cache first
  if (userCache[userId]) {
    return userCache[userId];
  }

  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error('User not found');
  }

  const user = await response.json();
  userCache[userId] = user;
  return user;
}

async function updateUser(userId, updates) {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });

  if (!response.ok) {
    throw new Error('Failed to update user');
  }

  const user = await response.json();
  userCache[userId] = user; // Update cache
  return user;
}

async function deleteUser(userId) {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'DELETE'
  });

  if (!response.ok) {
    throw new Error('Failed to delete user');
  }

  delete userCache[userId]; // Clear from cache
}

function clearCache() {
  Object.keys(userCache).forEach(key => delete userCache[key]);
}

module.exports = {
  getUser,
  updateUser,
  deleteUser,
  clearCache
};
