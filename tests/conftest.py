import pytest
from brownie import Contract


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="module")
def deployer(accounts):
    yield accounts[0]


@pytest.fixture(scope="module")
def alice(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def bob(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def keeper(accounts):
    yield accounts[3]


@pytest.fixture(scope="module")
def dcm(deployer, DaycareManager):
    yield deployer.deploy(DaycareManager)


@pytest.fixture(scope="module")
def adventuretime():
    yield Contract("0x0D4C98901563ca730332e841EDBCB801fe9F2551")


@pytest.fixture(scope="module")
def rarity():
    yield Contract("0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb")
