import time
from scripts.utilities import MockContract, get_account, get_contract
from brownie import RewardToken, TokenFarm
from brownie import network, config
from web3 import Web3

INITIAL_SUPPLY = Web3.toWei(1000, "ether")
KEPT_BALANCE = INITIAL_SUPPLY * 0.01


def deploy_token_farm_and_dapp_token():
    account = get_account()
    reward_token = RewardToken.deploy(INITIAL_SUPPLY, {"from": account})
    token_farm = TokenFarm.deploy(
        reward_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    # fill the reward token supply of the farm
    reward_token.transfer(
        token_farm.address, reward_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )

    weth_token = get_contract(MockContract.WETH_TOKEN)
    fau_token = get_contract(MockContract.FAU_TOKEN)
    allowed_token_addresses = {
        reward_token: get_contract(MockContract.DAI_USD_FEED),
        fau_token: get_contract(MockContract.DAI_USD_FEED),
        weth_token: get_contract(MockContract.ETH_USD_FEED),
    }

    add_allowed_tokens(token_farm, allowed_token_addresses, account)

    return token_farm, reward_token


def add_allowed_tokens(token_farm, allowed_tokens_price_feeds, account):
    for token in allowed_tokens_price_feeds:
        token_farm.addAllowedToken(token.address, {"from": account})
        token_farm.setTokenPriceFeed(
            token.address, allowed_tokens_price_feeds[token], {"from": account}
        )

    return token_farm


def main():
    deploy_token_farm_and_dapp_token()
    time.sleep(1)
