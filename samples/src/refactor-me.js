/**
 * Sample file with intentional code issues for refactoring practice
 *
 * Issues to find:
 * - Variable 'x' should have a descriptive name
 * - processOrder function is too long
 * - Unused variables: unusedCounter, tempData
 */

// Unused variable - should be removed
const unusedCounter = 0;

// Variable with poor naming - 'x' should be something like 'taxRate'
const x = 0.08;

// Another unused variable
let tempData = [];

// This function is too long and does too many things
// It should be split into smaller functions
function processOrder(items, customerName, address) {
  // Calculate subtotal
  let subtotal = 0;
  for (let i = 0; i < items.length; i++) {
    subtotal = subtotal + items[i].price * items[i].quantity;
  }

  // Apply discount if order is large
  let discount = 0;
  if (subtotal > 100) {
    discount = subtotal * 0.1;
  } else if (subtotal > 50) {
    discount = subtotal * 0.05;
  }

  // Calculate tax using 'x' (the tax rate)
  const tax = (subtotal - discount) * x;

  // Calculate total
  const total = subtotal - discount + tax;

  // Format the receipt
  let receipt = '=== ORDER RECEIPT ===\n';
  receipt = receipt + 'Customer: ' + customerName + '\n';
  receipt = receipt + 'Address: ' + address + '\n';
  receipt = receipt + '---\n';

  // Add each item to receipt
  for (let i = 0; i < items.length; i++) {
    receipt = receipt + items[i].name + ' x' + items[i].quantity;
    receipt = receipt + ' - $' + (items[i].price * items[i].quantity).toFixed(2) + '\n';
  }

  // Add totals to receipt
  receipt = receipt + '---\n';
  receipt = receipt + 'Subtotal: $' + subtotal.toFixed(2) + '\n';
  if (discount > 0) {
    receipt = receipt + 'Discount: -$' + discount.toFixed(2) + '\n';
  }
  receipt = receipt + 'Tax: $' + tax.toFixed(2) + '\n';
  receipt = receipt + 'Total: $' + total.toFixed(2) + '\n';

  return {
    subtotal: subtotal,
    discount: discount,
    tax: tax,
    total: total,
    receipt: receipt
  };
}

// Example usage
const sampleItems = [
  { name: 'Widget', price: 25.00, quantity: 2 },
  { name: 'Gadget', price: 15.50, quantity: 3 }
];

const result = processOrder(sampleItems, 'Jane Doe', '123 Main St');
console.log(result.receipt);

module.exports = { processOrder };
