# Dog

### **Purpose**

The Dog contract oversees the liquidation process. It monitors Vaults for undercollateralization and triggers auctions to sell collateral when necessary.

### Key Responsibilities

* Tracks undercollateralized Vaults.
* Incentivizes keepers to liquidate risky positions.

### Key Methods

*   `bark(ilk, urn, kpr)`\
    Initiates the liquidation process for a Vault (`urn`). Determines the amount of collateral to be auctioned and distributes liquidation rewards to keepers.

    hole: Maximum debt to liquidate per collateral type.
* `digs(ilk, rad)`\
  Adjusts internal debt balances after liquidation is completed.
* `file(ilk, what, data)`\
  Configures liquidation parameters, such as penalties and incentives.
  * Example Parameters:
    * `chop`: Liquidation penalty (e.g., 5% of the debt).
    *   `hole`: Maximum debt to liquidate per collateral type.
