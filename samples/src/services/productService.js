/**
 * Product service for e-commerce operations
 */

async function getAllProducts(filters = {}) {
  const params = new URLSearchParams(filters);
  const response = await fetch(`/api/products?${params}`);

  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }

  return response.json();
}

async function getProduct(productId) {
  const response = await fetch(`/api/products/${productId}`);

  if (!response.ok) {
    throw new Error('Product not found');
  }

  return response.json();
}

async function createProduct(productData) {
  const response = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(productData)
  });

  if (!response.ok) {
    throw new Error('Failed to create product');
  }

  return response.json();
}

async function updateProduct(productId, updates) {
  const response = await fetch(`/api/products/${productId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });

  if (!response.ok) {
    throw new Error('Failed to update product');
  }

  return response.json();
}

function formatPrice(cents) {
  return `$${(cents / 100).toFixed(2)}`;
}

function calculateDiscount(price, discountPercent) {
  return price * (1 - discountPercent / 100);
}

module.exports = {
  getAllProducts,
  getProduct,
  createProduct,
  updateProduct,
  formatPrice,
  calculateDiscount
};
