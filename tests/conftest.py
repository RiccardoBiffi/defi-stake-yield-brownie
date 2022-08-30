from web3 import Web3
import pytest
from brownie import AllowTokens


from scripts.utilities import get_account


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")


@pytest.fixture
def account():
    return get_account()


@pytest.fixture
def allow_tokens(account):
    return AllowTokens.deploy({"from": account})


@pytest.fixture
def token():
    return "0x345f9bFd2468f56CcCCb961c29Cf2a454E0812Cd"
