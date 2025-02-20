from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorV2_5Mock,
    Contract,
)

FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
sub_id = None


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2_5Mock,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract = config["networks"][network.show_active()][contract_name]
        """
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        """
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000
BASE_FEE = 100000000000000000
GAS_FEE = 1000000000
WEIPERUNITLINK = 4078168808521141


def deploy_mock(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("MockV3 deployed!")
    vrf_address = VRFCoordinatorV2_5Mock.deploy(
        BASE_FEE, GAS_FEE, WEIPERUNITLINK, {"from": account}
    )
    print("MockVRF deployed!")
    global sub_id
    sub_id = vrf_address.createSubscription()
    print("Subscription Id created...")
    # print(sub_id.info())
    sub_id = sub_id.return_value
    # sub_id = get_subid(vrf_address)
    # print("Subscription Id created...")
    print(sub_id)
    vrf_address.fundSubscription(sub_id, 100000000000000000)
    print("Subscription Funded...")
    # return sub_id


def get_subid():
    global sub_id
    """
    if len(VRFCoordinatorV2_5Mock) <= 1:
        sub_id = vrf_address.createSubscription()
        sub_id = sub_id.return_value
    """
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return sub_id
    else:
        return None


def fund_with_link(subID, account=None, amount=100000000000000000):
    # 0.1 LINK
    account = account if account else get_account()
    tx = get_contract("vrf_coordinator").fundSubscription(subID, amount)
    tx.wait(1)
    print("Contract Funded!")
    return tx
