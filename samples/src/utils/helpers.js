/**
 * Utility helper functions
 * Used throughout the application for common operations
 */

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// TODO: Add input validation
function parseJSON(str) {
  return JSON.parse(str);
}

function generateId() {
  return Math.random().toString(36).substring(2, 9);
}

module.exports = {
  formatDate,
  capitalize,
  debounce,
  parseJSON,
  generateId
};
