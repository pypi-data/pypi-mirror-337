"""Tests for type definitions."""
import pytest
from decimal import Decimal
from web3.types import ChecksumAddress
from comet_devx.types import (
    CometException,
    InsufficientFundsError,
    TransactionConfig,
    AssetInfo,
    Position,
    MarketInfo
)


def test_comet_exception():
    """Test CometException can be raised with message."""
    with pytest.raises(CometException) as exc_info:
        raise CometException("Test error")
    assert str(exc_info.value) == "Test error"


def test_insufficient_funds_error():
    """Test InsufficientFundsError inherits from CometException."""
    error = InsufficientFundsError("Not enough funds")
    assert isinstance(error, CometException)


def test_transaction_config_type():
    """Test TransactionConfig type accepts valid parameters."""
    config: TransactionConfig = {
        "from_": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "gas": 200000,
        "nonce": 1
    }
    assert isinstance(config, dict)
    assert "from_" in config
    assert "gas" in config


def test_asset_info_type():
    """Test AssetInfo type structure."""
    asset: AssetInfo = {
        "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "decimals": 18,
        "symbol": "USDC"
    }
    assert isinstance(asset, dict)
    assert all(key in asset for key in ["address", "decimals", "symbol"]) 