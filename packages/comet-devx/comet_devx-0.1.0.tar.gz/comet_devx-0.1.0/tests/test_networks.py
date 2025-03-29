"""Tests for network configuration."""
import pytest
from comet_devx.config.networks import get_network_config


def test_get_network_config_valid():
    """Test getting configuration for a valid network."""
    config = get_network_config("sepolia")
    assert isinstance(config, dict)
    assert "cometProxyAddress" in config
    assert config["cometProxyAddress"].startswith("0x")


def test_get_network_config_invalid():
    """Test getting configuration for an invalid network."""
    with pytest.raises(ValueError) as exc_info:
        get_network_config("invalid_network")
    assert "Unsupported network" in str(exc_info.value) 