"""Event handling system for Comet SDK."""
from typing import Callable, Dict, Any, Optional, List
from web3.types import EventData, LogReceipt
from web3.contract import Contract

from .types import CometException

class EventHandler:
    """Handler for Comet contract events.
    
    This class provides methods to:
    - Subscribe to events
    - Get historical events
    - Process event data
    """
    
    def __init__(self, contract: Contract):
        self.contract = contract
        self._event_filters: Dict[str, Any] = {}
        self._event_callbacks: Dict[str, List[Callable]] = {}

    async def subscribe(
        self,
        event_name: str,
        callback: Callable[[EventData], None],
        from_block: Optional[int] = None
    ) -> None:
        """Subscribe to a contract event.
        
        Args:
            event_name: Name of the event (e.g., 'Supply', 'Transfer')
            callback: Function to call when event is received
            from_block: Optional block number to start listening from
        """
        try:
            event = getattr(self.contract.events, event_name)
            event_filter = event.create_filter(fromBlock=from_block or 'latest')
            
            if event_name not in self._event_callbacks:
                self._event_callbacks[event_name] = []
            
            self._event_callbacks[event_name].append(callback)
            self._event_filters[event_name] = event_filter
            
        except Exception as e:
            raise CometException(f"Failed to subscribe to event {event_name}: {str(e)}")

    async def get_events(
        self,
        event_name: str,
        from_block: int,
        to_block: Optional[int] = None
    ) -> List[EventData]:
        """Get historical events.
        
        Args:
            event_name: Name of the event to query
            from_block: Start block number
            to_block: Optional end block number (defaults to 'latest')
            
        Returns:
            List of event data objects
        """
        try:
            event = getattr(self.contract.events, event_name)
            events = event.get_logs(
                fromBlock=from_block,
                toBlock=to_block or 'latest'
            )
            return events
        except Exception as e:
            raise CometException(f"Failed to get events for {event_name}: {str(e)}")

    async def process_events(self) -> None:
        """Process any new events for all subscriptions."""
        for event_name, event_filter in self._event_filters.items():
            try:
                events = event_filter.get_new_entries()
                callbacks = self._event_callbacks.get(event_name, [])
                
                for event in events:
                    for callback in callbacks:
                        callback(event)
                        
            except Exception as e:
                raise CometException(f"Failed to process events for {event_name}: {str(e)}")

    def unsubscribe(self, event_name: str) -> None:
        """Unsubscribe from an event.
        
        Args:
            event_name: Name of the event to unsubscribe from
        """
        if event_name in self._event_filters:
            self._event_filters[event_name].uninstall()
            del self._event_filters[event_name]
            del self._event_callbacks[event_name] 