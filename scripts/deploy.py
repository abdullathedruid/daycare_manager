import click
from brownie import accounts, DaycareManager, network


def main():
    print(f"Deploying to '{network.show_active()}' network")
    acct = accounts.load(click.prompt("account", type=click.Choice(accounts.load())))
    DaycareManager.deploy({"from": acct}, publish_source=True)
