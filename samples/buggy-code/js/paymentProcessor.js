// paymentProcessor.js - Sample code with intentional bugs for debugging practice
//
// Try: copilot --allow-all -p "Debug @samples/buggy-code/js/paymentProcessor.js"

const stripe = require('stripe');

// BUG 1: API key hardcoded (should be in env vars)
const stripeClient = stripe('sk_test_4eC39HqLyjWDarjtT1zdp7dc');

// BUG 2: No input validation
async function processPayment(amount, currency, cardToken) {
  const charge = await stripeClient.charges.create({
    amount: amount,
    currency: currency,
    source: cardToken,
  });
  return charge;
}

// BUG 3: Floating point arithmetic for money
function calculateTotal(items) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total; // Will have floating point errors: 0.1 + 0.2 = 0.30000000000000004
}

// BUG 4: No error handling
async function refund(chargeId, amount) {
  const refund = await stripeClient.refunds.create({
    charge: chargeId,
    amount: amount
  });
  return refund;
}

// BUG 5: Race condition in balance check
let accountBalance = 1000;

async function withdraw(amount) {
  if (accountBalance >= amount) {
    // Another request could modify accountBalance here
    await simulateNetworkDelay();
    accountBalance -= amount;
    return { success: true, newBalance: accountBalance };
  }
  return { success: false, reason: 'Insufficient funds' };
}

function simulateNetworkDelay() {
  return new Promise(resolve => setTimeout(resolve, 100));
}

// BUG 6: Sensitive data in logs
async function logTransaction(transaction) {
  console.log('Transaction:', JSON.stringify(transaction));
  // This logs credit card numbers and CVVs!
}

// BUG 7: SQL injection in receipt lookup
async function getReceipt(receiptId) {
  return db.query(`SELECT * FROM receipts WHERE id = '${receiptId}'`);
}

// BUG 8: Integer overflow risk
function convertCentsToDollars(cents) {
  return cents / 100;
}

function convertDollarsToCents(dollars) {
  return dollars * 100; // Can cause floating point issues
}

module.exports = {
  processPayment,
  calculateTotal,
  refund,
  withdraw,
  logTransaction,
  getReceipt,
  convertCentsToDollars,
  convertDollarsToCents
};
