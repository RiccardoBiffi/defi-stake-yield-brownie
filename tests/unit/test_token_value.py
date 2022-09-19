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


# region setTokenPriceFeed
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


# todo missing tests

# endregion
