from scripts.utils import get_account
from brownie import config, interface, network

def get_weth():
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.01 * 10 ** 18})
    tx.wait(1)
    print(f"Deposited 0.1 Eth for 0.1 Weth")
    pass

def main():
    get_weth()
    pass

