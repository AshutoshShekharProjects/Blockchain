from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, config, network


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        config["networks"][network.show_active()]["subscription_id"],
        config["networks"][network.show_active()]["keyHash"],
        {"from": account},
    )


def main():
    deploy_and_create()
