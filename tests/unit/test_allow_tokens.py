import brownie
from brownie import AllowTokens
from brownie import network
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()

    # Act
    at = AllowTokens.deploy({"from": account})

    # Assert
    assert at.address != None


# region addAllowedToken
def test_add_allowed_tokens_success(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act
    tx = allow_tokens.addAllowedToken(token, {"from": account})

    # Assert
    assert allow_tokens.allowedTokens(0) == token
    assert tx.events["AllowToken"]["admin"] == account
    assert tx.events["AllowToken"]["token"] == token


def test_add_allowed_tokens_fail_already_allowed(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    allow_tokens.addAllowedToken(token, {"from": account})

    # Act

    # Assert
    with brownie.reverts("The token is already allowed"):
        allow_tokens.addAllowedToken(token, {"from": account})


def test_add_allowed_tokens_fail_not_owner(allow_tokens, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    not_owner = get_account(1)

    # Act

    # Assert
    with brownie.reverts():
        allow_tokens.addAllowedToken(token, {"from": not_owner})


# endregion

# region removeAllowedToken
def test_remove_allowed_token_success(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    allow_tokens.addAllowedToken(token, {"from": account})

    # Act
    tx = allow_tokens.removeAllowedToken(token, {"from": account})

    # Assert
    with brownie.reverts():
        assert allow_tokens.allowedTokens(0)
    assert tx.events["DisallowToken"]["admin"] == account
    assert tx.events["DisallowToken"]["token"] == token


def test_remove_allowed_token_fail_already_unallowed(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act

    # Assert
    with brownie.reverts("The token is already unallowed"):
        allow_tokens.removeAllowedToken(token, {"from": account})


def test_remove_allowed_token_fail_not_owner(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    not_owner = get_account(1)

    # Act
    allow_tokens.addAllowedToken(token, {"from": account})

    # Assert
    with brownie.reverts():
        allow_tokens.removeAllowedToken(token, {"from": not_owner})


# endregion

# region isTokenAllowed
def test_check_token_allowed_true(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    allow_tokens.addAllowedToken(token, {"from": account})

    # Act
    answer = allow_tokens.isTokenAllowed(token, {"from": account})

    # Assert
    assert answer == True


def test_check_token_allowed_false(allow_tokens, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act
    answer = allow_tokens.isTokenAllowed(token, {"from": account})

    # Assert
    assert answer == False


# endregion
