from brownie import RewardToken
from brownie import network
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_token():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    total_supply = 10**18

    # Act
    rt = RewardToken.deploy(total_supply, {"from": account})

    # Assert
    assert rt.symbol() == "RWD"
    assert rt.decimals() == 18
    assert rt.name() == "Reward"
    assert rt.totalSupply() == total_supply
    assert rt.balanceOf(account) == rt.totalSupply()
