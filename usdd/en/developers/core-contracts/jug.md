# Jug

### **Purpose**

Calculates and accrues stability fees on minted USDD. These fees ensure protocol sustainability and discourage excessive borrowing.

### Key Responsibilities

* Accumulate stability fees for particular collateral types .
* Adjusts debt levels to reflect accrued interest.

### Key Methods

* `drip(ilk)`\
  Accrues stability fees for the specified collateral type since its last accrual timestamp (`rho`). Calls `Vat.fold` to update the accumulated debt multiplier, system debt, and the Vow’s surplus balance.
*   **`file(what, data)` / `file(ilk, what, data)`**

    Configures global or collateral-specific parameters.

    * **`duty`**: The collateral-specific, per-second stability fee contribution, stored as a ray-scaled integer with a scaling factor of `10^27`. It is not an annualized percentage.
    * **`base`**: The global, per-second stability fee contribution, also stored as a ray-scaled integer.

    In the standard Jug calculation, the effective per-second compounding factor is **`(base + duty) / 10^27`**. Do not pass an annualized percentage directly as `duty`.
