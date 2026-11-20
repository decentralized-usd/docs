# Clip

### **Purpose**

Handles collateral auctions, where liquidated collateral is sold to cover bad debt. CLIP ensures auctions operate fairly and efficiently using a Dutch auction mechanism.

### Key Responsibilities

* Conducts auctions for liquidated collateral.
* Ensures participants receive fair prices.

### Key Methods

* `kick(tab, lot, usr, kpr)`\
  Starts an auction with a debt amount (`tab`), collateral amount (`lot`), and Vault owner (`usr`).
  * Example Use: Kicking off an auction for a liquidated Vault.
* `redo(id, kpr)`\
  Allows keepers to reinitialize a stale auction, ensuring auction prices remain relevant.
*   `take(id, amt, max, who, data)`<br>

    Purchases collateral from an active auction at the current auction price, subject to the buyer’s maximum acceptable price.

    * `id`: The auction ID.
    * `amt`: The maximum amount of collateral to purchase, expressed with wad precision (`10^18` scaling).
    * `max`: The maximum acceptable price in USDD per unit of collateral, expressed with ray precision (`10^27` scaling).
    * `who`: The address receiving the collateral in the Vat and, when applicable, the callback recipient.
    * `data`: Data passed to the optional callback. An empty value disables the callback.
*   **`yank(id)`**

    Cancels an active auction through an authorized call, for example during emergency shutdown or a governance action. Removes the auction, updates the liquidation accounting, and transfers the remaining collateral balance in the Vat to the caller.

    * `id`: The auction ID.
    * **Access restriction:** Only authorized addresses with `wards[msg.sender] == 1` can call this function.
* `file(what, data)`\
  Configures auction parameters and contract addresses, including keeper incentives, reset durations, and the price calculator (`calc`).
  * Example Parameters:
    * `tip`: Fixed incentive for starting an auction.
    * `calc`: Price calculator contract address, configured through the address overload of `file(what, data)`. The calculator determines the decay model and holds its parameters. For `StairstepExponentialDecrease`, `cut` is a ray-scaled price multiplier applied once per `step` seconds. For `ExponentialDecrease`, `cut` applies every second. Read the active calculator and its parameters for the selected collateral and network.
