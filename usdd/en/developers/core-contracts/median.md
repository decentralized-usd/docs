# Median

### **Purpose**

It provides the protocol’s trusted reference price.

### Key Responsibilities

* Maintains a whitelist of price feed contracts which are authorized to post price updates.
* Computes and updates the stored value when a new list of prices is received.

### Key Methods

* `poke()`\
  Updates price from whitelisted providers.
* `peek()`\
  Returns the stored price (`uint256`) and a validity flag (`bool`).
