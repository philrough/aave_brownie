from importlib_metadata import NullFinder
from scripts.aave_borrow import get_account, get_asset_price, get_lending_pool, get_weth, approve_erc20
from brownie import config, network
from web3 import Web3

def test_get_account():
    # Arrange / Act
    account = get_account()

    #Assert
    assert account is not None

def test_get_asset_price():
    # Arrange / #Act
    erc20_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    #Assert
    assert erc20_eth_price > 0

def test_get_lending_pool():
    # Arrange / Act
    lending_pool = get_lending_pool()

    # Assert
    assert lending_pool is not None

def test_approve_erc20():
    # Arrange
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    get_weth()
    lending_pool = get_lending_pool()

    # Act
    approve_tx = approve_erc20(Web3.toWei('0.01', 'ether'), lending_pool.address, erc20_address, account)

    # Assert
    assert approve_tx is not False

def test_get_borrowable_date():
    # Arrange / Act - Assumes that the test account has already deposited / borrowed
    account = get_account()
    lending_pool = get_lending_pool()
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")

    # Assert
    assert available_borrow_eth > 0
    assert total_collateral_eth > 0
    assert total_debt_eth > 0

def test_deposit():
    # Arrange - Assumes test account has weth token - Only test on mainnet-fork - kovan not stable
    account = get_account()
    lending_pool = get_lending_pool()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    # Act
    balance_before = account.balance()
    tx = lending_pool.deposit(
        erc20_address, Web3.toWei('0.01', 'ether'), account.address, 0, {"from": account}
    )
    tx.wait(1)


    # Assert
    assert tx is not False
    assert account.balance() < balance_before 

