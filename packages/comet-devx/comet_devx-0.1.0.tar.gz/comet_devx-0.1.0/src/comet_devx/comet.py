"""
Core Comet SDK implementation for interacting with Compound V3.

This module provides the main Comet class that handles all interactions with
the Compound V3 protocol, including supply, borrow, and repay operations.
"""
import json
import pathlib
from typing import Optional, Union, Dict, Any

from web3 import Web3
from web3.contract import Contract
from web3.types import TxReceipt, Wei, ChecksumAddress

from .config.networks import get_network_config, NetworkConfig
from .types import (
    CometException,
    InsufficientFundsError,
    TransactionConfig,
    Position,
    MarketInfo
)
from .events import EventHandler


class Comet:
    """
    Main class for interacting with Compound V3 (Comet) protocol.
    
    This class provides methods to:
    - Supply collateral to Comet
    - Borrow the base asset
    - Repay borrowed assets
    - Query positions and market data
    
    Attributes:
        web3: Web3 instance for blockchain interaction
        network: Network identifier (e.g., 'sepolia')
        contract: Web3 contract instance for Comet
        account: Active account address
    """

    def __init__(
        self,
        network: str,
        web3: Web3,
        account: Optional[ChecksumAddress] = None
    ) -> None:
        """
        Initialize the Comet SDK.

        Args:
            network: Network identifier (e.g., 'sepolia')
            web3: Web3 instance
            account: Optional account address for transactions

        Raises:
            CometException: If contract initialization fails
        """
        self.web3 = web3
        self.network = network
        self.account = account
        self.network_config = get_network_config(network)

        # Load ABI
        try:
            abi_path = pathlib.Path(__file__).parent / "abis" / "CometInterface.json"
            with open(abi_path) as f:
                self.abi = json.load(f)
        except Exception as e:
            raise CometException(f"Failed to load ABI: {str(e)}")

        # Initialize contract
        try:
            self.contract = self.web3.eth.contract(
                address=self.network_config["cometProxyAddress"],
                abi=self.abi
            )
        except Exception as e:
            raise CometException(f"Failed to initialize contract: {str(e)}")

        # Initialize event handler
        self.events = EventHandler(self.contract)

    async def supply(
        self,
        asset: ChecksumAddress,
        amount: Wei,
        config: Optional[TransactionConfig] = None
    ) -> TxReceipt:
        """
        Supply an asset to Comet as collateral.

        Args:
            asset: The ERC20 token address to supply
            amount: Amount to supply (in smallest units)
            config: Optional transaction configuration

        Returns:
            TxReceipt: The transaction receipt

        Raises:
            InsufficientFundsError: If insufficient token balance
            CometException: If the transaction fails
        """
        if not self.account:
            raise CometException("No account set for transaction")

        tx_config = {
            "from": self.account,
            **(config or {})
        }

        try:
            # Build transaction
            tx = self.contract.functions.supply(
                asset,
                amount
            ).build_transaction(tx_config)
            
            # Real transaction handling
            signed_tx = self.web3.eth.account.sign_transaction(
                tx,
                private_key=self.web3.eth.account._private_key
            )
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        except Exception as e:
            if "insufficient funds" in str(e).lower():
                raise InsufficientFundsError("Insufficient token balance")
            raise CometException(f"Supply failed: {str(e)}")

    async def borrow(
        self,
        amount: Wei,
        config: Optional[TransactionConfig] = None
    ) -> TxReceipt:
        """
        Borrow base asset from Comet.

        Args:
            amount: Amount to borrow (in smallest units)
            config: Optional transaction configuration

        Returns:
            TxReceipt: The transaction receipt

        Raises:
            InsufficientFundsError: If insufficient collateral
            CometException: If the transaction fails
        """
        if not self.account:
            raise CometException("No account set for transaction")

        tx_config = {
            "from": self.account,
            **(config or {})
        }

        try:
            # Get base token - remove await since it's a mock in tests
            base_token = self.contract.functions.baseToken().call()
            
            tx = self.contract.functions.withdraw(
                base_token,
                amount
            ).build_transaction(tx_config)
            
            # Real transaction handling
            signed_tx = self.web3.eth.account.sign_transaction(
                tx,
                private_key=self.web3.eth.account._private_key
            )
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
        except Exception as e:
            if "insufficient collateral" in str(e).lower():
                raise InsufficientFundsError("Insufficient collateral")
            raise CometException(f"Borrow failed: {str(e)}")

    async def repay(
        self,
        amount: Wei,
        config: Optional[TransactionConfig] = None
    ) -> TxReceipt:
        """
        Repay borrowed base asset to Comet.

        Args:
            amount: Amount to repay (in smallest units)
            config: Optional transaction configuration

        Returns:
            TxReceipt: The transaction receipt

        Raises:
            InsufficientFundsError: If insufficient base asset balance
            CometException: If the transaction fails
        """
        if not self.account:
            raise CometException("No account set for transaction")

        tx_config = {
            "from": self.account,
            **(config or {})
        }

        try:
            # Get base token - remove await since it's a mock in tests
            base_token = self.contract.functions.baseToken().call()
            
            tx = self.contract.functions.supply(
                base_token,
                amount
            ).build_transaction(tx_config)
            
            # Real transaction handling
            signed_tx = self.web3.eth.account.sign_transaction(
                tx,
                private_key=self.web3.eth.account._private_key
            )
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
        except Exception as e:
            if "insufficient funds" in str(e).lower():
                raise InsufficientFundsError("Insufficient base asset balance")
            raise CometException(f"Repay failed: {str(e)}")

    def get_network(self) -> str:
        """Simple test method to verify the setup"""
        return f"Connected to {self.network} network"
