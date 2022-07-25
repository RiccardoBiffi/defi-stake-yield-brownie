from enum import Enum
from brownie import network, accounts, config
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


class MockContract(Enum):
    LINK_TOKEN = "link_token"
    VRF_COORDINATOR = "vrf_coordinator"


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]  # Ganache's first account
    if id:
        return accounts.load(id)

    # mainnet
    return accounts.add(config["wallets"]["from_key"])


# initializer = box.store, 1,2,3
def encode_function_data(
    init_function=None, *args
):  # *args means "any other arguments" in type and number
    """
    Encodes the function call into bytes to work with an initializer.

    Args:
        init_function ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Ex: "box.store"
        Default to None.

        args (Any, optional):
        The arguments to pass to the initializer function.

    Returns:
        [bytes]: Initializer function and arguments encoded into bytes.
    """
    if len(args) == 0 or init_function == None:
        return eth_utils.to_bytes(
            hexstr="0x"
        )  # blank hex means "no arguments" to caller
    return init_function.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implentation_addr,
    proxy_admin=None,
    initializer=None,
    *args  # can be None
):
    if proxy_admin:
        if initializer:
            encoded_initializer = encode_function_data(initializer, *args)
            # we have an initializer, so we upgrade and call it
            tx = proxy_admin.upgradeAndCall(
                proxy,
                new_implentation_addr,
                encoded_initializer,
                {"from": account},
            )
        else:
            tx = proxy_admin.upgrade(proxy, new_implentation_addr, {"from": account})
    else:
        if initializer:
            encoded_initializer = encode_function_data(initializer, *args)
            # we have an initializer, so we upgrade and call it
            tx = proxy.upgradeToAndCall(
                new_implentation_addr,
                encoded_initializer,
                {"from": account},
            )
        else:
            tx = proxy.upgradeTo(new_implentation_addr, {"from": account})

    return tx
