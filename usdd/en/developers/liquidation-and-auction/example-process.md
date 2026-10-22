# Example Process

1. **Collateral Deposit and Minting**\
   In this example, assume a liquidation threshold of 130% and a liquidation penalty of 10%. A user deposits collateral worth $1,500 and mints 1,000 USDD, resulting in a collateralization ratio of 150%.
2. **Market Downturn and Collateralization Ratio Drop**\
   Due to a market downturn, the collateral value drops to $1,200, reducing the collateralization ratio to 120%, which is below the liquidation threshold of 130%.
3. **Liquidation Triggered**\
   The system automatically flags the Vault for liquidation to protect the protocol from losses.
4. **Collateral Auction Begins**
   1. The liquidation engine starts an auction for the $1,200 worth of collateral.
   2. The auction follows a Dutch auction mechanism, where the price starts at a high initial value and gradually decreases over time until a bidder accepts the price or the auction ends.
5. **Keeper Participation**
   1. Keepers, who are incentivized participants, place bids during the auction.
   2. A Keeper bids an amount of USDD equal to the debt ($1,000) plus the liquidation penalty (10%), totaling $1,100.
   3. The Keeper wins the auction by accepting the current auction price for the collateral.
6. **Collateral Settlement**
   1. The protocol retains $1,100 worth of USDD to cover the debt and liquidation penalty.
   2. Any remaining collateral value (after deducting the amount sold during the auction) is refunded to the user.
7. **Auction Outcome**
   1. The Keeper receives the collateral at the auction price. For example, if the auction price is $0.95 per unit of collateral, the Keeper receives collateral valued at $1,157.89 ($1,100 ÷ $0.95).
   2. The user retains any excess collateral that wasn't required to cover the debt and penalty.

This process ensures the protocol remains solvent while providing opportunities for Keepers to acquire collateral at competitive prices and protecting users by refunding surplus collateral.

\\
