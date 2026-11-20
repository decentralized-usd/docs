# Spot

### **Purpose**

Ensures the protocol receives real-time, reliable price data for all collateral types. SPOT determines whether Vaults meet collateralization requirements.

### Key Responsibilities

* Retrieves and updates collateral prices.
* Enforces collateralization thresholds for system stability.

### Key Methods

* `poke(ilk)`\
  Updates the system with the latest price for a specific collateral type.
  * Example Use: Updating the TRX price when markets fluctuate.
* `file(ilk, what, data)`\
  Configures parameters such as the liquidation ratio (`mat`).
  * Example Use: Setting mat to 150%, requiring 1.5x collateral for every USDD minted.
