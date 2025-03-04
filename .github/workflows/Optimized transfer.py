from web3 import Web3
import os
import logging
import time

# Logging setup
logging.basicConfig(filename="transactions.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Load environment variables
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
TOKEN_ADDRESSES = os.getenv("TOKEN_ADDRESSES").split(",")  # Multiple ERC-20 tokens
RECIPIENTS = os.getenv("RECIPIENT_ADDRESSES").split(",")   # Multiple recipients
AMOUNTS = os.getenv("TRANSFER_AMOUNTS").split(",")         # Amounts for each token

# Connect to blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

# ERC-20 Contract ABI (Minimal)
ERC20_ABI = [
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
]

def send_tokens(token_address, recipient, amount):
    try:
        contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
        nonce = web3.eth.get_transaction_count(account.address)
        
        tx = contract.functions.transfer(recipient, int(amount)).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 60000,  # Optimized gas limit
            'gasPrice': web3.eth.gas_price,  # Auto-fetch gas price
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash_str = web3.to_hex(tx_hash)

        print(f"✅ Sent {amount} tokens ({token_address}) to {recipient}: {tx_hash_str}")
        logging.info(f"Transaction: {tx_hash_str} | Token: {token_address} | Recipient: {recipient}")
        
        time.sleep(3)  # Avoid nonce issues
    
    except Exception as e:
        logging.error(f"❌ Failed transfer of {amount} tokens ({token_address}) to {recipient}: {str(e)}")

# Batch transfer for each token & recipient
for token, amount in zip(TOKEN_ADDRESSES, AMOUNTS):
    for recipient in RECIPIENTS:
        send_tokens(Web3.to_checksum_address(token), Web3.to_checksum_address(recipient), amount)
