import time
from scripts.utilities import MockContract, get_account, get_contract
from brownie import RewardToken, TokenFarm
from brownie import network, config
from web3 import Web3
import yaml
import json
import os
import shutil

INITIAL_SUPPLY = Web3.toWei(1000, "ether")
KEPT_BALANCE = (INITIAL_SUPPLY / 2) * 0.01


def publish_source_policy():
    return config["networks"][network.show_active()].get("verify", False)


def deploy_token_farm_and_dapp_token(update_FE=False):
    account = get_account()
    # print(RewardToken.get_verification_info())
    # print(TokenFarm.get_verification_info())

    reward_token = RewardToken.deploy(
        INITIAL_SUPPLY,
        {"from": account},
        publish_source=publish_source_policy(),
    )
    token_farm = TokenFarm.deploy(
        reward_token.address,
        {"from": account},
        publish_source=publish_source_policy(),
    )

    # fill the reward token supply of the farm
    reward_token.transfer(
        token_farm.address,
        reward_token.balanceOf(account) - KEPT_BALANCE,
        {"from": account},
    )

    weth_token = get_contract(MockContract.WETH_TOKEN)
    fau_token = get_contract(MockContract.FAU_TOKEN)

    tf_allowed_token_addresses_and_feeds = {
        reward_token: get_contract(MockContract.DAI_USD_FEED),
        fau_token: get_contract(MockContract.DAI_USD_FEED),
        weth_token: get_contract(MockContract.ETH_USD_FEED),
    }

    rt_allowed_token_addresses_and_feeds = {
        reward_token: get_contract(MockContract.DAI_USD_FEED),
        fau_token: get_contract(MockContract.DAI_USD_FEED),
    }

    add_allowed_tokens(token_farm, tf_allowed_token_addresses_and_feeds, account)
    add_allowed_tokens(reward_token, rt_allowed_token_addresses_and_feeds, account)

    if update_FE:
        update_fron_end()
    return token_farm, reward_token


def add_allowed_tokens(token_farm, allowed_tokens_price_feeds, account):
    for token in allowed_tokens_price_feeds:
        token_farm.addAllowedToken(token.address, {"from": account})
        token_farm.setTokenPriceFeed(
            token.address, allowed_tokens_price_feeds[token], {"from": account}
        )

    return token_farm


def update_fron_end():
    # Send to the front-end brownie-config as JSON
    with open("brownie-config.yaml", "r") as bc_yaml:
        config_dict = yaml.load(bc_yaml, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as bc_json:
            json.dump(config_dict, bc_json)

    # Send the build folder
    copy_folder_to_front_end("./build", "./front_end/src/chain_info")

    print("Front-end updated")


def copy_folder_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    deploy_token_farm_and_dapp_token(True)
    time.sleep(1)


if __name__ == "__main__":
    main()
