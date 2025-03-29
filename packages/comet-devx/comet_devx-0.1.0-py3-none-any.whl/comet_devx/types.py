"""
Type definitions for the Comet SDK.

This module contains all the type definitions needed for interacting with
Compound V3 (Comet), including contract types, transaction types, and custom exceptions.
"""
from typing import TypedDict, Dict, Any, Optional, Union
from decimal import Decimal
from web3.types import TxReceipt, Wei, HexStr, ChecksumAddress


class CometException(Exception):
    """Base exception for Comet SDK."""
    pass


class InsufficientFundsError(CometException):
    """Raised when there are insufficient funds for a transaction."""
    pass


class TransactionConfig(TypedDict, total=False):
    """Transaction configuration parameters.
    
    Attributes:
        from_: The sender's address
        gas: Gas limit for the transaction
        gasPrice: Gas price in Wei
        nonce: Transaction nonce
        value: Amount of ETH to send
    """
    from_: ChecksumAddress
    gas: Optional[int]
    gasPrice: Optional[Wei]
    nonce: Optional[int]
    value: Optional[Wei]


class AssetInfo(TypedDict):
    """Information about an asset in Comet.
    
    Attributes:
        address: The asset's contract address
        decimals: Number of decimals the asset uses
        symbol: The asset's symbol (e.g., 'USDC')
    """
    address: ChecksumAddress
    decimals: int
    symbol: str


class Position(TypedDict):
    """User position information.
    
    Attributes:
        principal: The principal amount
        baseBalance: Base asset balance
        baseTrackingIndex: Base tracking index
        baseTrackingAccrued: Accrued base tracking
    """
    principal: Decimal
    baseBalance: Decimal
    baseTrackingIndex: Decimal
    baseTrackingAccrued: Decimal


class MarketInfo(TypedDict):
    """Market information and parameters.
    
    Attributes:
        baseToken: Base token information
        baseTokenPriceFeed: Price feed address for base token
        supplyKink: Supply rate kink point
        supplyPerYearInterestRateBase: Base supply interest rate
        supplyPerYearInterestRateSlopeLow: Supply rate slope below kink
        supplyPerYearInterestRateSlopeHigh: Supply rate slope above kink
    """
    baseToken: AssetInfo
    baseTokenPriceFeed: ChecksumAddress
    supplyKink: Decimal
    supplyPerYearInterestRateBase: Decimal
    supplyPerYearInterestRateSlopeLow: Decimal
    supplyPerYearInterestRateSlopeHigh: Decimal
