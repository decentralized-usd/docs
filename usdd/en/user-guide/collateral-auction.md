# Collateral Auction

When a Vault is liquidated, its collateral is moved into an auction process. Users can bid on the collateral at auction prices, potentially securing profits. The auction uses a Dutch auction model, where the price gradually decreases over time until a buyer places a bid or the auction ends.

#### Steps to Participate in an Auction

1.  **Navigate to the Auction Page**\
    Visit the Auction Page to explore ongoing auctions.

    <figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>
2. **View Auction Details**
   1. Access the details of the Vault undergoing auction.
   2. Review information about the collateral, debt, and current auction price.
3. **Stake USDD for Auction Participation**
   1. To bid, you must first stake USDD, which will be used for purchasing collateral in the auction.
   2. Staked USDD can be withdrawn anytime if not used for a bid.
4. **Place Your Bid**
   1. Enter the amount of USDD you wish to spend on the auction.
   2.  The platform will display the following estimates:

       1.  The estimated amount of collateral you will receive at the quoted auction price:

           **Collateral Quantity = Input USDD Amount ÷ Auction Price**
       2.  Potential net Profit: The estimated profit from selling the purchased collateral at the quoted market price, after deducting the USDD spent and estimated transaction fees:

           **Potential Net Profit = Collateral Quantity × Market Price − Input USDD Amount − Estimated Transaction Fees**

       Equivalently:

       **Potential Net Profit = (Input USDD Amount ÷ Auction Price) × Market Price − Input USDD Amount − Estimated Transaction Fees**

       Auction Price and Market Price are expressed in **USDD per unit of collateral**. Estimated Transaction Fees must also be expressed in **USDD**.

       **Example**

       If you spend **100 USDD** at an auction price of **2 USDD per unit**, you will receive **50 units** of collateral. At a market price of **3 USDD per unit**, your estimated profit before transaction fees is:

       **(100 ÷ 2) × 3 − 100 = 50 USDD**

       These estimates are not guaranteed returns. Actual results depend on the final auction execution price, the sale price, and applicable fees.

       <figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>
5. **Monitor Auction Prices**
   1. Since the auction follows the Dutch auction model, the price decreases over time.
   2. The page displays the current auction price and the time remaining before it decreases further.
6. **Complete the Purchase**
   1. If your bid is successful, you will acquire the collateral, which can be sold or used as desired. Any collateral obtained from auctions is stored in the liquidation auction account and can be withdrawn to the winning bidders’ wallet.
   2. The actual profit will depend on the market price when you decide to sell the collateral.

Participating in auctions is an excellent way to acquire assets at competitive prices and contribute to the USDD ecosystem.
