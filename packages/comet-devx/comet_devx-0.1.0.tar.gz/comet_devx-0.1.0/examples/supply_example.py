"""Example of supplying collateral to Compound V3."""
import asyncio
from web3 import Web3
from comet_devx import Comet

async def main():
    # Initialize Web3 with your provider
    w3 = Web3(Web3.HTTPProvider('YOUR_RPC_URL'))
    
    # Your account details
    account = "YOUR_ACCOUNT_ADDRESS"
    
    # Initialize Comet
    comet = Comet('sepolia', w3, account=account)
    
    # USDC address on Sepolia
    usdc_address = "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8"
    
    # Supply 100 USDC (with 6 decimals)
    try:
        tx_receipt = await comet.supply(
            asset=usdc_address,
            amount=100 * 10**6  # 100 USDC
        )
        print(f"Supply successful! Transaction hash: {tx_receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"Supply failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
