import time
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_subid,
)
from brownie import Lottery, config, network, VRFCoordinatorV2_5Mock


def deploy_lottery():
    account = get_account()
    # sub_id = get_subid(VRFCoordinatorV2_5Mock[-1])
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed"),
        get_contract("vrf_coordinator"),
        (
            get_subid()
            if get_subid() != None
            else config["networks"][network.show_active()]["subscription_id"]
        ),
        {"from": account},
        # publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Deployed Lottery!")
    sub_id = get_subid()
    print(sub_id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        get_contract("vrf_coordinator").addConsumer(sub_id, lottery)
        # VRFCoordinatorV2_5Mock[-1].addConsumer(sub_id, lottery.address)
        print("Consumer added!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntryFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    """
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        tx = fund_with_link(sub_id)
        tx.wait(1)
    get_contract("vrf_coordinator").addConsumer(
        config["networks"][network.show_active()]["subscription_id"], lottery.address
    )
    """
    end_transaction = lottery.endLottery({"from": account})
    end_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner")
    print("End...")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
