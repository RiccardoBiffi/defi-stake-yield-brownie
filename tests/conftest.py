from web3 import Web3
import pytest
from brownie import RewardToken, MockDAI, AllowTokens, TokenValue, MockV3Aggregator
from scripts.utilities import get_account


@pytest.fixture
def amount():
    return Web3.toWei(1, "ether")


@pytest.fixture
def supply():
    return Web3.toWei(1000, "ether")


@pytest.fixture
def decimals():
    return 18


@pytest.fixture
def account():
    return get_account()


@pytest.fixture
def allow_tokens(account):
    return AllowTokens.deploy({"from": account})


@pytest.fixture
def token_value(account):
    return TokenValue.deploy({"from": account})


@pytest.fixture
def reward_token(supply, account):
    return RewardToken.deploy(supply, {"from": account})


@pytest.fixture
def dai(amount, account, reward_token):
    mock_dai = MockDAI.deploy({"from": account})
    mock_dai.mint(amount, {"from": account})
    mock_dai.approve(reward_token.address, amount, {"from": account})
    return mock_dai


@pytest.fixture
def token_value_DAI(decimals, account):
    return MockV3Aggregator.deploy(decimals, 1 * 10**decimals, {"from": account})


@pytest.fixture
def token_value_ETH(decimals, account):
    return MockV3Aggregator.deploy(decimals, 1560 * 10**decimals, {"from": account})


@pytest.fixture
def token():
    return "0x345f9bFd2468f56CcCCb961c29Cf2a454E0812Cd"
