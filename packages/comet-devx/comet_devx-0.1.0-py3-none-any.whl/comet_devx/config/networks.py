"""
Network configuration for Comet SDK.

This module defines the network configurations and types for interacting with
Compound V3 (Comet) on different networks.
"""
from typing import TypedDict, Dict


class NetworkConfig(TypedDict):
    """Network configuration type.
    
    Attributes:
        cometProxyAddress: The address of the Comet proxy contract
    """
    cometProxyAddress: str


NETWORKS: Dict[str, NetworkConfig] = {
    "sepolia": {
        "cometProxyAddress": "0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"
    }
    # Additional networks can be added here
}


def get_network_config(network: str) -> NetworkConfig:
    """Get the configuration for a specific network.
    
    Args:
        network: The network identifier (e.g., 'sepolia')
        
    Returns:
        NetworkConfig: The network configuration
        
    Raises:
        ValueError: If the network is not supported
    """
    if network not in NETWORKS:
        raise ValueError(f"Unsupported network: {network}")
    return NETWORKS[network]
