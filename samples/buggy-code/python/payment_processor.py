# payment_processor.py - Sample code with intentional bugs for debugging practice
#
# Try: copilot --allow-all -p "Debug @samples/buggy-code/python/payment_processor.py"

import os
import sqlite3
from decimal import Decimal

# BUG 1: API key hardcoded (should be in env vars)
STRIPE_API_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


# BUG 2: No input validation
def process_payment(amount, currency, card_token):
    import stripe
    stripe.api_key = STRIPE_API_KEY
    charge = stripe.Charge.create(
        amount=amount,
        currency=currency,
        source=card_token
    )
    return charge


# BUG 3: Floating point arithmetic for money
def calculate_total(items):
    total = 0.0
    for item in items:
        total += item['price'] * item['quantity']
    return total  # Will have floating point errors: 0.1 + 0.2 = 0.30000000000000004


# BUG 4: No error handling
def refund(charge_id, amount):
    import stripe
    stripe.api_key = STRIPE_API_KEY
    refund = stripe.Refund.create(
        charge=charge_id,
        amount=amount
    )
    return refund


# BUG 5: Race condition in balance check
account_balance = 1000.0

async def withdraw(amount):
    global account_balance
    if account_balance >= amount:
        # Another request could modify account_balance here
        import asyncio
        await asyncio.sleep(0.1)  # Simulate network delay
        account_balance -= amount
        return {"success": True, "new_balance": account_balance}
    return {"success": False, "reason": "Insufficient funds"}


# BUG 6: Sensitive data in logs
def log_transaction(transaction):
    print(f"Transaction: {transaction}")
    # This logs credit card numbers and CVVs!


# BUG 7: SQL injection in receipt lookup
def get_receipt(receipt_id):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM receipts WHERE id = '{receipt_id}'")
    return cursor.fetchone()


# BUG 8: Integer overflow risk / precision loss
def convert_cents_to_dollars(cents):
    return cents / 100


def convert_dollars_to_cents(dollars):
    return dollars * 100  # Can cause floating point issues


# BUG 9: Insecure random for transaction IDs (Python-specific)
import random

def generate_transaction_id():
    # random is not cryptographically secure!
    return random.randint(100000, 999999)


# BUG 10: eval() on user input (Python-specific)
def calculate_discount(formula, price):
    # User-controlled formula passed to eval - code injection!
    discount = eval(formula)
    return price - discount


# BUG 11: Shell injection (Python-specific)
def export_transactions(filename):
    # User-controlled filename in shell command
    os.system(f"cat transactions.log > {filename}")


# BUG 12: YAML unsafe load (Python-specific)
import yaml

def load_pricing_config(config_string):
    # yaml.load without Loader is vulnerable to code execution
    return yaml.load(config_string)  # Should use yaml.safe_load()
