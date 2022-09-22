import brownie
from brownie import TokenValue
from brownie import network
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()

    # Act
    tv = TokenValue.deploy({"from": account})

    # Assert
    assert tv.address != None


def test_set_token_price_feed_success(token_value, account, token, token_value_ETH):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act
    tx = token_value.setTokenPriceFeed(
        token, token_value_ETH.address, {"from": account}
    )

    # Assert
    assert token_value.token_priceFeed(token) == token_value_ETH.address
    assert tx.events["AddedPriceFeed"]["admin"] == account
    assert tx.events["AddedPriceFeed"]["token"] == token
    assert tx.events["AddedPriceFeed"]["priceFeed"] == token_value_ETH.address


def test_remove_token_price_feed_success(token_value, account, token):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act
    tx = token_value.removeTokenPriceFeed(token, {"from": account})

    # Assert
    assert token_value.token_priceFeed(token) == brownie.ZERO_ADDRESS
    assert tx.events["RemovedPriceFeed"]["admin"] == account
    assert tx.events["RemovedPriceFeed"]["token"] == token


def test_get_token_value_success(
    token_value, account, token, token_value_ETH, ETH_price, decimals
):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    token_value.setTokenPriceFeed(token, token_value_ETH.address, {"from": account})

    # Act
    (r_price, r_decimals) = token_value.getTokenValue(token, {"from": account})

    # Assert
    assert r_price == ETH_price
    assert r_decimals == decimals


def test_get_value_from_token_success(
    token_value, account, amount, token, token_value_ETH, ETH_price, decimals
):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    token_value.setTokenPriceFeed(token, token_value_ETH.address, {"from": account})

    # Act
    value = token_value.getValueFromToken(amount, token, {"from": account})

    # Assert
    assert value == amount * ETH_price / 10**decimals


def test_get_token_from_value_success(
    token_value, account, amount, token, token_value_ETH, ETH_price, decimals
):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    token_value.setTokenPriceFeed(token, token_value_ETH.address, {"from": account})

    # Act
    r_token = token_value.getTokenFromValue(amount, token, {"from": account})

    # Assert
    assert r_token == amount * 10**decimals / ETH_price
