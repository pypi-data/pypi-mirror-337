"""Tests for Comet class."""
import pytest
from web3 import Web3
from web3.types import Wei, TxReceipt
from unittest.mock import Mock, patch

from comet_devx.comet import Comet
from comet_devx.types import CometException, InsufficientFundsError

@pytest.fixture
def web3_mock():
    """Create a mock Web3 instance."""
    w3 = Mock(spec=Web3)
    # Mock the eth account
    w3.eth = Mock()
    w3.eth.account = Mock()
    w3.eth.contract = Mock()
    return w3

@pytest.fixture
def mock_tx_receipt():
    """Create a mock transaction receipt."""
    return {
        'transactionHash': '0x123...',
        'blockNumber': 1234,
        'status': 1
    }

@pytest.fixture
def comet(web3_mock):
    """Create a Comet instance with mocked Web3."""
    return Comet(
        "sepolia",
        web3_mock,
        account="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )

def test_comet_initialization():
    """Test basic Comet class initialization"""
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    comet = Comet("sepolia", w3)
    assert comet.get_network() == "Connected to sepolia network"

@pytest.mark.asyncio
async def test_supply(comet, web3_mock, mock_tx_receipt):
    """Test supplying assets."""
    # Setup mock chain of calls
    mock_fn = Mock()
    mock_fn.build_transaction.return_value = {
        'to': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'data': '0x',
        'gas': 200000,
    }
    comet.contract.functions.supply = Mock(return_value=mock_fn)
    
    # Mock transaction handling
    web3_mock.eth.account.sign_transaction = Mock()
    web3_mock.eth.send_raw_transaction = Mock()
    web3_mock.eth.wait_for_transaction_receipt = Mock(return_value=mock_tx_receipt)

    # Test successful supply
    result = await comet.supply(
        "0x1234567890123456789012345678901234567890",
        Wei(1000000)
    )
    
    assert result == mock_tx_receipt
    comet.contract.functions.supply.assert_called_once()

@pytest.mark.asyncio
async def test_borrow(comet, web3_mock, mock_tx_receipt):
    """Test borrowing assets."""
    # Setup mock chain of calls
    mock_base_token = Mock()
    mock_base_token.call.return_value = "0x1234567890123456789012345678901234567890"
    comet.contract.functions.baseToken = Mock(return_value=mock_base_token)
    
    mock_withdraw = Mock()
    mock_withdraw.build_transaction.return_value = {
        'to': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'data': '0x',
        'gas': 200000,
    }
    comet.contract.functions.withdraw = Mock(return_value=mock_withdraw)
    
    # Mock transaction handling
    web3_mock.eth.account.sign_transaction = Mock()
    web3_mock.eth.send_raw_transaction = Mock()
    web3_mock.eth.wait_for_transaction_receipt = Mock(return_value=mock_tx_receipt)

    # Test successful borrow
    result = await comet.borrow(Wei(1000000))
    
    assert result == mock_tx_receipt
    comet.contract.functions.withdraw.assert_called_once()

@pytest.mark.asyncio
async def test_repay(comet, web3_mock, mock_tx_receipt):
    """Test repaying borrowed assets."""
    # Setup mock chain of calls
    mock_base_token = Mock()
    mock_base_token.call.return_value = "0x1234567890123456789012345678901234567890"
    comet.contract.functions.baseToken = Mock(return_value=mock_base_token)
    
    mock_supply = Mock()
    mock_supply.build_transaction.return_value = {
        'to': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'data': '0x',
        'gas': 200000,
    }
    comet.contract.functions.supply = Mock(return_value=mock_supply)
    
    # Mock transaction handling
    web3_mock.eth.account.sign_transaction = Mock()
    web3_mock.eth.send_raw_transaction = Mock()
    web3_mock.eth.wait_for_transaction_receipt = Mock(return_value=mock_tx_receipt)

    # Test successful repay
    result = await comet.repay(Wei(1000000))
    
    assert result == mock_tx_receipt
    comet.contract.functions.supply.assert_called_once()

@pytest.mark.asyncio
async def test_supply_insufficient_funds(comet, web3_mock):
    """Test supplying assets with insufficient funds."""
    # Mock contract function to raise error
    mock_fn = Mock()
    mock_fn.build_transaction.side_effect = Exception("insufficient funds for transfer")
    comet.contract.functions.supply = Mock(return_value=mock_fn)

    # Test insufficient funds error
    with pytest.raises(InsufficientFundsError):
        await comet.supply(
            "0x1234567890123456789012345678901234567890",
            Wei(1000000)
        )
