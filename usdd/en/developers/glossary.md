# Glossary

## General

* `wad`: some quantity of tokens, usually as a fixed point integer with 18 decimal places.
* `ray`: a fixed point integer, with 27 decimal places.
* `rad`: a fixed point integer, with 45 decimal places.
* `file`: administer some configuration value
* `auth`: check whether an address can call this method
* `wards`: an address that is allowed to call authored methods
* `rely`: allow an address to call authored methods
* `deny`: disallow an address from calling authored methods
* `Authority:` checks whether an address can call this method

## Vat

* `hope`: enable wish for a pair of addresses.
* `nope`: disable wish for a pair of addresses.
* `init`: start stability fee collection for a particular collateral type
* `slip`：modify a user's collateral balance.
* `move`：transfer stablecoin between users.
* `frob`：modify a Vault.
* `grab`：liquidate a Vault.
* `heal`：create / destroy equal quantities of stablecoin and system debt (vice).
* `suck`：mint unbacked stablecoin (accounted for with vice).
* `fold`：modify the debt multiplier, creating / destroying corresponding debt.
* `ilk`：a collateral type.
  * `art`：total normalized stablecoin debt.
  * `rate`：stablecoin debt multiplier (accumulated stability fees).
  * `line`：the debt ceiling for a specific collateral type.
  * `dust`：the minimum possible debt of a Vault.

## Vow

* `Sin`: the total amount of debt in the queue.
* `Ash`: the total amount of on-auction debt.
* `wait`: debt auction delay.
* `sump`: debt auction bid size, i.e. the fixed debt quantity to be covered by any one debt auction
* `dump`: debt auction lot size, i.e. the starting amount of MKR offered to cover the lot/sump
* `bump`: surplus auction lot size, i.e. the fixed surplus quantity to be sold by any one surplus auction
* `hump`: surplus buffer, must be exceeded before surplus auctions are possible

## Dog

* `bark`: A vault’s all debt is taken when this liquidation function is called.
* `ilk`
  * `chop`: Liquidation Penalty
  * `hole`: Max USDD needed to cover debt+fees of active auctions per ilk
  * `dirt`: Amt USDD needed to cover debt+fees of active auctions per ilk

## Clip

* `buf`: Multiplicative factor to increase starting price
* `tail`: Time elapsed before auction reset
* `cusp`: Percentage drop before auction reset
* `chip`: Percentage of tab to suck from vow to incentivize keepers
* `tip`: Flat fee to suck from vow to incentivize keepers
* `chost`: Cache the ilk dust times the ilk chop to prevent excessive SLOADs
* `sale`
  * `pos`: Index in active array
  * `tab`:USDD to raise
  * `usr`: Liquidated CDP
  * `tic`: Auction start time
  * `top`: Starting price

## Jug

* **`duty`**: Collateral-specific, per-second stability fee contribution, stored with ray precision (`10^27` scaling).
* **`base`**: Global, per-second stability fee contribution, stored with ray precision (`10^27` scaling).
* **`rho`**: Unix timestamp of the last stability fee accrual for a collateral type.

## Median

* `orcl(usr: address)` : oracles whitelist of the prices (whitelisted via governance / the authorized parties).
* `bud(usr: address):` readers whitelist.
* `val:` the price (private) must be read with `read()` or `peek()`
* `age`: the Block timestamp of last price `val` update.
* `wat:` the price oracles type (ex: TRXUSD) / tells us what the type of asset is.
* `bar`: the Minimum writers quorum for poke / min number of valid messages you need to have to update the price.

## OSM

* `src` : address of DSValue that the OSM will read from
* `hop` : time delay between poke calls (uint16); defaults to ONE\_HOUR
* `cur` : Feed struct that holds the current price value
* `nxt` : Feed struct that holds the next price value
* `bud` : mapping from address to uint256; whitelists feed readers
