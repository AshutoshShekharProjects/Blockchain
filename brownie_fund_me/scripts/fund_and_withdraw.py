from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    # entrance_fee = fund_me.getEntranceFee()
    entrance_fee = fund_me.getEntranceFee()
    print(f"Current price is {fund_me.getPrice()}")
    print(f"The current entrance fee is {entrance_fee}")
    print("Funding...")
    fund_me.fund({"from": account, "value": entrance_fee})
    print("Funding Successfull!")


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing...")
    fund_me.withdraw({"from": account})
    print("Amount is Withdrawen!")


def main():
    fund()
    withdraw()
