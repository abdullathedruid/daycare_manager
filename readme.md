# Daycare Manager

Deployed at [0xf1bf34E46ECf465591B7a7fA9635E4C583174fa3](https://ftmscan.com/address/0xf1bf34e46ecf465591b7a7fa9635e4c583174fa3)

Framework to allow users to create permissionless bots to adventure time
You can register your summoners with `registerDaycare()` and will pay a fee of 0.1 FTM per summoner per day.

You will need to approve the adventure time contract `0x0D4C98901563ca730332e841EDBCB801fe9F2551` in order to allow users to adventure on your behalf

Anybody will be able to adventure on your behalf in a trustless manner, and in doing so, will receive the 0.1 FTM fee.

Advanced coders will be able to generate scripts/bots that can adventure on behalf of users by calling `executeDaycare()`
Hopefully the economic incentives add up.

Feel free to deploy to re-deploy the contract with a different fee if the price of FTM varies significantly.


Notes:
 - You cannot unregister once you have registered -> I would recommend only registering small number of days at a time
 - This isn't audited.
 - `adventureTime.adventureTime(_summonerIds)` will revert if ANY of the summoner ids is invalid.
