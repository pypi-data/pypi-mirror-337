"""Example of listening to Compound V3 events."""
import asyncio
from web3 import Web3
from comet_devx import Comet

async def handle_supply_event(event):
    """Handle Supply events."""
    args = event['args']
    print(f"Supply Event:")
    print(f"  Supplier: {args['supplier']}")
    print(f"  Amount: {args['amount']}")

async def handle_withdraw_event(event):
    """Handle Withdraw events."""
    args = event['args']
    print(f"Withdraw Event:")
    print(f"  Src: {args['src']}")
    print(f"  Amount: {args['amount']}")

async def main():
    # Initialize Web3 with your provider
    w3 = Web3(Web3.HTTPProvider('YOUR_RPC_URL'))
    
    # Initialize Comet
    comet = Comet('sepolia', w3)
    
    # Subscribe to events
    await comet.events.subscribe('Supply', handle_supply_event)
    await comet.events.subscribe('Withdraw', handle_withdraw_event)
    
    print("Listening for events... Press Ctrl+C to exit")
    
    try:
        while True:
            await comet.events.process_events()
            await asyncio.sleep(1)  # Poll every second
    except KeyboardInterrupt:
        print("\nStopping event listener...")

if __name__ == "__main__":
    asyncio.run(main()) 