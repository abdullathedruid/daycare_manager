import brownie
import pytest
from brownie.test import given, strategy
from brownie import chain
import math

# EXECUTE DAYCARE

fee_per_execution = 1e17


@given(summoner_id=strategy("uint256"))
def test_execute_without_setup(dcm, summoner_id, keeper):
    with brownie.reverts():
        dcm.executeDaycare([summoner_id], {"from": keeper})


@pytest.fixture(scope="module")
def alice_summoned(alice, adventuretime, rarity):
    tx = rarity.summon(1, {"from": alice})
    summoner_id = tx.events["summoned"]["summoner"]
    rarity.approve(adventuretime.address, summoner_id, {"from": alice})
    yield summoner_id


def test_execute_with_setup(dcm, alice, keeper, alice_summoned, rarity):
    balance = keeper.balance()
    dcm.registerDaycare(
        [alice_summoned], [1], {"from": alice, "value": fee_per_execution}
    )
    dcm.executeDaycare([alice_summoned], {"from": keeper})
    assert rarity.xp(alice_summoned) == 250 * 1e18
    assert balance + fee_per_execution == keeper.balance()


def test_execute_twice_no_break(dcm, alice, keeper, alice_summoned):
    dcm.registerDaycare(
        [alice_summoned], [2], {"from": alice, "value": 2 * fee_per_execution}
    )
    dcm.executeDaycare([alice_summoned], {"from": keeper})
    with brownie.reverts():
        dcm.executeDaycare([alice_summoned], {"from": keeper})


def test_execute_twice_with_break(dcm, alice, keeper, alice_summoned, rarity):
    balance = keeper.balance()
    dcm.registerDaycare(
        [alice_summoned], [2], {"from": alice, "value": 2 * fee_per_execution}
    )
    dcm.executeDaycare([alice_summoned], {"from": keeper})
    chain.sleep(math.floor(1 * 60 * 60 * 24.1))
    chain.mine()
    dcm.executeDaycare([alice_summoned], {"from": keeper})
    assert balance + 2 * fee_per_execution == keeper.balance()
    assert rarity.xp(alice_summoned) == 500 * 1e18
