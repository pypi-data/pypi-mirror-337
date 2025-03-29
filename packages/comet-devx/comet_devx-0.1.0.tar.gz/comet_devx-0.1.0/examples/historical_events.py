"""Example of fetching historical events from Compound V3."""
import asyncio
from web3 import Web3
from comet_devx import Comet
from datetime import datetime

async def main():
    # Initialize Web3 with your provider
    w3 = Web3(Web3.HTTPProvider('YOUR_RPC_URL'))
    
    # Initialize Comet
    comet = Comet('sepolia', w3)
    
    # Get events from the last 1000 blocks
    current_block = await w3.eth.block_number
    from_block = current_block - 1000
    
    try:
        # Get Supply events
        supply_events = await comet.events.get_events(
            'Supply',
            from_block=from_block
        )
        
        print(f"\nFound {len(supply_events)} Supply events:")
        for event in supply_events:
            args = event['args']
            block = await w3.eth.get_block(event['blockNumber'])
            timestamp = datetime.fromtimestamp(block['timestamp'])
            print(f"\nBlock {event['blockNumber']} ({timestamp})")
            print(f"  Supplier: {args['supplier']}")
            print(f"  Amount: {args['amount']}")
            
    except Exception as e:
        print(f"Failed to fetch events: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 