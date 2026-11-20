# Vat

### **Purpose**

The core accounting contract of the protocol, VAT tracks system-wide balances, including user Vaults, collateral types, and debt. It ensures that all collateral and debt are properly accounted for and enforces system solvency.

### Key Responsibilities

* Tracks collateral and debt balances for all users and collateral types.
* Ensures Vault operations (e.g., minting and repaying USDD) adhere to protocol parameters.
* Integrates with other contracts to trigger auctions or manage liquidations.

### Key Methods

* `slip(ilk, usr, wad)`\
  Adjusts the balance of a specific collateral type (`ilk`) for a user (`usr`).
  * Example Use: Adding or removing collateral from a user's Vault.
* `frob(ilk, u, v, w, dink, dart)`\
  Adjusts collateral (`dink`) and debt (`dart`) for a Vault.
  * Example Use: Minting new USDD or repaying debt.
* `grab(ilk, u, v, w, dink, dart)`\
  Executes adjustments on collateral and debt during liquidation.
* `fold(ilk, u, rate)`\
  Increase the `Ilk.rate` with rate, and hence the debt balances of all Vaults collateralized with the specified Ilk are updated implicitly.
* `file(what, data) / file(ilk, what, data)`\
  Sets or updates system-wide parameters like debt ceilings, stability fees, or collateralization thresholds.
  * Example Use: Setting a collateral type’s maximum mintable USDD.
