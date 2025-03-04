from web3 import Web3
import os

# Load environment variables
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
RECIPIENT = os.getenv("RECIPIENT_ADDRESS")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")

# Connect to BSC
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Check connection
assert w3.is_connected(), "Failed to connect to BSC node!"

# Load sender account
account = w3.eth.account.from_key(PRIVATE_KEY)
sender = account.address

# BEP-20 Transfer function ABI
token_abi = [
    {"constant": False, "inputs": [{"name": "recipient", "type": "address"}, {"name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

# Load token contract
token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)

# Transfer function
def transfer_tokens(amount):
    amount_wei = w3.to_wei(amount, 'ether')  # Adjust for token decimals
    nonce = w3.eth.get_transaction_count(sender)
    
    txn = token_contract.functions.transfer(RECIPIENT, amount_wei).build_transaction({
        'chainId': 56,  # BSC Mainnet
        'gas': 200000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': nonce
    })
    
    signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent! TX Hash: {tx_hash.hex()}")

# Run transfer
if __name__ == "__main__":
    transfer_tokens(1)  # Set amount to send
