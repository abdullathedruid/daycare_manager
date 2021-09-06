import brownie
from brownie.test import given, strategy

# REGISTER DAYCARE

fee_per_execution = 1e17


@given(
    summoner_id=strategy("uint256"),
    days=strategy("uint256", min_value=1, max_value=365),
)
def test_add_single_summoner(dcm, alice, summoner_id, days):
    if days * fee_per_execution < 100e18:
        dcm.registerDaycare(
            [summoner_id], [days], {"from": alice, "value": days * fee_per_execution}
        )
        assert dcm.daysPaid(summoner_id) == days


@given(
    summoner_idA=strategy("uint256"),
    summoner_idB=strategy("uint256"),
    daysA=strategy("uint256", min_value=1, max_value=365),
    daysB=strategy("uint256", min_value=1, max_value=365),
)
def test_add_two_summoners(dcm, alice, summoner_idA, summoner_idB, daysA, daysB):
    fee = (daysA + daysB) * fee_per_execution
    if fee < 100e18:
        dcm.registerDaycare(
            [summoner_idA, summoner_idB], [daysA, daysB], {"from": alice, "value": fee}
        )
        if summoner_idA == summoner_idB:
            assert dcm.daysPaid(summoner_idA) == daysA + daysB
        else:
            assert dcm.daysPaid(summoner_idA) == daysA
            assert dcm.daysPaid(summoner_idB) == daysB


@given(
    summoner_id=strategy("uint256"),
    days=strategy("uint256", min_value=1, max_value=365),
)
def test_insufficient_fee(dcm, alice, summoner_id, days):
    insufficient_amount = days * 1e16
    with brownie.reverts("DCM: Insufficient fee"):
        dcm.registerDaycare(
            [summoner_id], [days], {"from": alice, "value": insufficient_amount}
        )
        print(insufficient_amount, days * fee_per_execution)


@given(
    summoner_id=strategy("uint256"),
    days=strategy("uint256", min_value=1, max_value=365),
)
def test_invalid_length(dcm, alice, summoner_id, days):
    with brownie.reverts("DCM: Invalid lengths"):
        dcm.registerDaycare(
            [summoner_id, summoner_id],
            [days],
            {"from": alice, "value": days * fee_per_execution},
        )


@given(summoner_id=strategy("uint256"))
def test_zero_days(dcm, alice, summoner_id):
    with brownie.reverts("DCM: Cannot daycare for 0 days"):
        dcm.registerDaycare([summoner_id], [0], {"from": alice})
