from enum import Enum
from brownie import Contract, network, accounts, config
from brownie import MockV3Aggregator, MockWETH, MockDAI
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
WETH_STARTING_PRICE = 2000 * 10**DECIMALS
DAO_STARTING_PRICE = 1 * 10**DECIMALS


class MockContract(Enum):
    WETH_TOKEN = "weth_token"
    FAU_TOKEN = "fau_token"
    ETH_USD_FEED = "eth_usd_feed"
    DAI_USD_FEED = "dai_usd_feed"


contract_to_mock = {
    MockContract.WETH_TOKEN: MockWETH,
    MockContract.FAU_TOKEN: MockDAI,
    MockContract.ETH_USD_FEED: MockV3Aggregator,
    MockContract.DAI_USD_FEED: MockV3Aggregator,
}


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def get_contract(contract_enum):
    """
    Ottiene il contract specificato.
    Se la blockchain è un fork o esterna, lo prende leggendo l'address da brownie-config;
    altrimenti, se siamo su una blockchain locale, viene deployato un mock e restituito.

    Args:
        contract_enum (MockContract): enum del contratto da ottenere

    Returns:
        brownie.network.contract.ProjectContract : l'ultima versione deployata del contratto,
        che può essere un mock o un contratto "reale" già presente sul network
    """
    contract_type = contract_to_mock[contract_enum]

    if is_local_blockchain():
        if len(contract_type) == 0:  # contratto mai deployato
            deploy_mock(contract_enum)
        contract = contract_type[-1]  # prendo l'ultimo contratto deployato

    else:
        # il contratto esiste già nella blockchain (testnet o fork)
        contract_address = config["networks"][network.show_active()][
            contract_enum.value
        ]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mock(contract_enum):
    """
    Deploya il contratto in input.
    """
    print(f"Deploying mock {contract_enum.value} to network: {network.show_active()}")
    if contract_enum == MockContract.WETH_TOKEN:
        MockWETH.deploy({"from": get_account()})
    elif contract_enum == MockContract.FAU_TOKEN:
        MockDAI.deploy({"from": get_account()})
    elif contract_enum == MockContract.DAI_USD_FEED:
        MockV3Aggregator.deploy(DECIMALS, WETH_STARTING_PRICE, {"from": get_account()})
    elif contract_enum == MockContract.FAU_TOKEN:
        MockV3Aggregator.deploy(DECIMALS, DAO_STARTING_PRICE, {"from": get_account()})

    print(f"Mock {contract_enum.value} deployed!\n")


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
    *args,  # can be None
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
