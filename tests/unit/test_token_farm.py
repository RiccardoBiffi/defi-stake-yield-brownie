from brownie import TokenFarm
from brownie import network, exceptions
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_farm():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()

    # Act
    tf = TokenFarm.deploy({"from": account})

    # Assert
    assert tf.address != None


def test_can_allow_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"

    # Act
    tf = TokenFarm.deploy({"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Assert
    assert tf.allowedTokens(0) == "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"


def test_check_token_allowed_true():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    tf = TokenFarm.deploy({"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Act
    answer = tf.isTokenAllowed(token_addr, {"from": account})

    # Assert
    assert answer == True


def test_check_token_allowed_false():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    other_token_addr = "0x9294cBDC3dbcd3E11a07892e7bA5c3394048Cc51"
    tf = TokenFarm.deploy({"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Act
    answer = tf.isTokenAllowed(other_token_addr, {"from": account})

    # Assert
    assert answer == False


def test_stake_token_success():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    amount = 10**18
    tf = TokenFarm.deploy({"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Act
    tf.stakeTokens(amount, token_addr, {"from": account})

    # Assert
    tf.stakedTokens() == amount


def test_stake_token_fail_low_amount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    tf = TokenFarm.deploy({"from": account})

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tf.stakeTokens(0, token_addr, {"from": account})


def test_stake_token_fail_not_allowed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    tf = TokenFarm.deploy({"from": account})

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tf.stakeTokens(10**18, token_addr, {"from": account})
