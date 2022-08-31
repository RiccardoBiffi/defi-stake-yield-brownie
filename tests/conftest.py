from web3 import Web3
import pytest
from brownie import AllowTokens, TokenValue, MockV3Aggregator
from scripts.utilities import get_account


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")


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
def token_value_DAI(decimals, account):
    return MockV3Aggregator.deploy(decimals, 1 * 10**decimals, {"from": account})


@pytest.fixture
def token_value_ETH(decimals, account):
    return MockV3Aggregator.deploy(decimals, 1560 * 10**decimals, {"from": account})


@pytest.fixture
def token():
    return "0x345f9bFd2468f56CcCCb961c29Cf2a454E0812Cd"
