from brownie import RewardToken, MockDAI
from brownie import network
import brownie
from web3 import Web3
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_contract():
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
    assert rt.buyableRWD() == total_supply / 2
    assert rt.balanceOf(account) == rt.totalSupply() / 2


def test_buy_success(reward_token, dai, amount, token_value_DAI, account):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    # transfer all coins to RewardToken
    reward_token.transfer(
        reward_token.address, reward_token.balanceOf(account), {"from": account}
    )
    reward_token.addAllowedToken(dai.address, {"from": account})
    reward_token.setTokenPriceFeed(dai.address, token_value_DAI, {"from": account})
    reward_token.setTokenPriceFeed(
        reward_token.address, token_value_DAI, {"from": account}
    )
    initial_supply = reward_token.balanceOf(reward_token.address, {"from": account})
    old_buyable_RWD = reward_token.buyableRWD()

    # Act
    tx = reward_token.buy(amount, dai.address, {"from": account})

    # Assert
    assert dai.balanceOf(account) == 0
    assert dai.balanceOf(reward_token.address) == amount
    assert reward_token.tokenWithDeposits(0) == dai.address
    assert reward_token.token_deposit(dai.address) == amount
    assert reward_token.balanceOf(reward_token.address) < initial_supply
    assert reward_token.balanceOf(account) > 0
    assert reward_token.buyableRWD() == old_buyable_RWD - amount
    assert tx.events["Exchange"]["from"] == account
    assert tx.events["Exchange"]["exchangeToken"] == dai.address
    assert tx.events["Exchange"]["amountIn"] == amount
    assert tx.events["Exchange"]["amountRwdOut"] == reward_token.balanceOf(account)


def test_buy_fail_token_not_allowed(reward_token, dai, amount, account):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act

    # Assert
    with brownie.reverts("Cannot buy RWD with this token"):
        reward_token.buy(amount, dai.address, {"from": account})


def test_buy_fail_amount_is_zero(reward_token, dai, account):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    reward_token.addAllowedToken(dai.address, {"from": account})
    # Act

    # Assert
    with brownie.reverts("Amount must be more than 0 tokens"):
        reward_token.buy(0, dai.address, {"from": account})


def test_buy_fail_allowance_not_approved(reward_token, dai, amount, account):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    dai.approve(reward_token.address, 0, {"from": account})
    reward_token.addAllowedToken(dai.address, {"from": account})

    # Act

    # Assert
    with brownie.reverts("ERC20: insufficient allowance"):
        reward_token.buy(amount, dai.address, {"from": account})
