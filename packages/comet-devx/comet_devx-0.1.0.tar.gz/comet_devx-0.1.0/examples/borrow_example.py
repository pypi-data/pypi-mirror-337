"""Example of borrowing from Compound V3."""
import asyncio
from web3 import Web3
from comet_devx import Comet
from comet_devx.types import InsufficientFundsError

async def main():
    # Initialize Web3 with your provider
    w3 = Web3(Web3.HTTPProvider('YOUR_RPC_URL'))
    
    # Your account details
    account = "YOUR_ACCOUNT_ADDRESS"
    
    # Initialize Comet
    comet = Comet('sepolia', w3, account=account)
    
    # Borrow 10 USDC (with 6 decimals)
    try:
        tx_receipt = await comet.borrow(10 * 10**6)  # 10 USDC
        print(f"Borrow successful! Transaction hash: {tx_receipt['transactionHash'].hex()}")
    except InsufficientFundsError:
        print("Insufficient collateral to borrow")
    except Exception as e:
        print(f"Borrow failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
