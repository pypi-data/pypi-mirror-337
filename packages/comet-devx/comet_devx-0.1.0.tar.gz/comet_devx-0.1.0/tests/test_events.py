"""Tests for event handling system."""
import pytest
from unittest.mock import Mock, AsyncMock
from web3.types import EventData
from web3.contract import Contract

from comet_devx.events import EventHandler
from comet_devx.types import CometException

@pytest.fixture
def mock_contract():
    """Create a mock contract with event capabilities."""
    contract = Mock(spec=Contract)
    # Mock the events attribute
    contract.events = Mock()
    return contract

@pytest.fixture
def event_handler(mock_contract):
    """Create an EventHandler instance with mocked contract."""
    return EventHandler(mock_contract)

@pytest.fixture
def mock_event_filter():
    """Create a mock event filter."""
    filter_mock = Mock()
    filter_mock.get_new_entries.return_value = [
        {
            'event': 'Supply',
            'args': {
                'supplier': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
                'amount': 1000000
            }
        }
    ]
    return filter_mock

@pytest.mark.asyncio
async def test_subscribe(event_handler, mock_contract):
    """Test subscribing to an event."""
    # Mock the event object
    mock_event = Mock()
    mock_event.create_filter.return_value = Mock()
    mock_contract.events.Supply = mock_event

    # Create a test callback
    callback = Mock()

    # Subscribe to event
    await event_handler.subscribe('Supply', callback)

    # Verify
    assert 'Supply' in event_handler._event_callbacks
    assert callback in event_handler._event_callbacks['Supply']
    mock_event.create_filter.assert_called_once_with(fromBlock='latest')

@pytest.mark.asyncio
async def test_get_events(event_handler, mock_contract):
    """Test getting historical events."""
    # Mock the event object
    mock_event = Mock()
    mock_event.get_logs.return_value = [
        {'event': 'Supply', 'args': {'amount': 1000}}
    ]
    mock_contract.events.Supply = mock_event

    # Get events
    events = await event_handler.get_events('Supply', from_block=1234)

    # Verify
    assert len(events) == 1
    mock_event.get_logs.assert_called_once_with(
        fromBlock=1234,
        toBlock='latest'
    )

@pytest.mark.asyncio
async def test_process_events(event_handler, mock_contract, mock_event_filter):
    """Test processing new events."""
    # Setup mock event filter
    event_handler._event_filters['Supply'] = mock_event_filter
    
    # Setup callback
    callback = Mock()
    event_handler._event_callbacks['Supply'] = [callback]

    # Process events
    await event_handler.process_events()

    # Verify callback was called with event data
    callback.assert_called_once()
    event_data = callback.call_args[0][0]
    assert event_data['event'] == 'Supply'
    assert event_data['args']['amount'] == 1000000

@pytest.mark.asyncio
async def test_unsubscribe(event_handler, mock_contract, mock_event_filter):
    """Test unsubscribing from events."""
    # Setup mock event filter
    event_handler._event_filters['Supply'] = mock_event_filter
    event_handler._event_callbacks['Supply'] = [Mock()]

    # Unsubscribe
    event_handler.unsubscribe('Supply')

    # Verify
    assert 'Supply' not in event_handler._event_filters
    assert 'Supply' not in event_handler._event_callbacks
    mock_event_filter.uninstall.assert_called_once()

@pytest.mark.asyncio
async def test_subscribe_error_handling(event_handler, mock_contract):
    """Test error handling in subscribe method."""
    # Mock the event object to raise an exception
    mock_event = Mock()
    mock_event.create_filter.side_effect = Exception("Failed to create filter")
    mock_contract.events.Supply = mock_event

    # Attempt to subscribe
    with pytest.raises(CometException) as exc_info:
        await event_handler.subscribe('Supply', Mock())
    
    assert "Failed to subscribe to event Supply" in str(exc_info.value)

@pytest.mark.asyncio
async def test_process_events_error_handling(event_handler, mock_event_filter):
    """Test error handling in process_events method."""
    # Setup mock event filter to raise an exception
    mock_event_filter.get_new_entries.side_effect = Exception("Failed to get entries")
    event_handler._event_filters['Supply'] = mock_event_filter

    # Attempt to process events
    with pytest.raises(CometException) as exc_info:
        await event_handler.process_events()
    
    assert "Failed to process events for Supply" in str(exc_info.value) 