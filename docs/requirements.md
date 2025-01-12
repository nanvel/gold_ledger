# Reddit

https://www.reddit.com/r/SaaS/comments/1hy5nbr/looking_for_a_cofounder_web_developer_for_my_saas/

I have a family business,
wherein we own a wholesale jewelry segment, and sell jewelry to retailers.

But the catch is tracking products and payments is tough, so I thought to build a tool.

Purpose: The software will help wholesalers (suppliers) and retailers track their payments 
and manage the goods sold (by suppliers) or received (by retailers).

Currently, my uncles and friends who do the same business use tally prime, which costs them around INR 9000 per year or INR 27000 (forever).
Yet, they are not able to properly do accounting and track their payments and products,

If we could build such a stuff properly, I expect an easy MRR of $10K.
Considering I have more than 5000 contacts of wholesalers and expect easily most of them 50-60% of them buying our product!

Homepage Options:
- I am a Supplier
- I am a Retailer

## Supplier Features

Login or Signup Flow: Enter Supplier Office Name (Office ID) and Password.

If Office ID does not exist, create a new account automatically and log in.

If Office ID exists, check the password and log in if it matches.

Page 1: Products Sold Search for retailers by their Store ID (via search bar or dropdown).
View all products sold to a specific retailer.

Page 2: Payment Acceptance Search for retailers by their Store ID.

### Add Product Functionality

Form fields:
- Product Name
- Automatic Current Date
- Weight
- Quality
- Rate Per Gram
- Total Amount
- Custom Fields (dynamic labels/values)
- Picture Upload

Show the product details in a list/card format.

Products will appear on the retailer’s side as "Product Given - Unverified"
until verified by the retailer, after which it updates to "Product Given - Verified." 

### Payment Acceptance 

View Date-Wise Payments sent by the retailer.

Record payment acceptance:
- Cash Payment: Enter amount.
- Goods Payment: Enter Weight, Quality, Rate, and Total Amount.

Payments will appear on the retailer’s side as "Payment Paid - Verified" once accepted.

Show Total Amount Left to be Paid by the retailer.

## Retailer Features

Login or Signup Flow: Enter Store Name (ID) and Password.

If Store ID does not exist, create a new account automatically and log in.

If Store ID exists, check the password and log in if it matches.

Page 1: Products Acceptance View product details added by suppliers:
- Supplier Name
- Product Name
- Date
- Weight
- Quality
- Rate
- Total Cost

Verify products using an "Accept Product" button, which updates the status for both supplier and retailer.

Page 2: Payment Given Record payments sent to suppliers:
- Cash Payment: Enter amount and date.
- Goods Payment: Enter Weight, Quality, Rate, and Total Amount.

View transaction details: Payments appear as "Payment Paid - Verified" once accepted by the supplier.
Show Total Amount Left to be Paid to the supplier.
