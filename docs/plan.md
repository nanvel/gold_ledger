# Plan

MVP v3:
- [x] deploy
- [x] session -> account
- [x] show shop id
- [ ] convert to date
- [ ] due date
- [ ] search by id if only number provided
- [ ] error messages in login/register form
- [ ] Products, Payments, Settings
- [ ] retailer views
  - [ ] supplier page
  - [ ] products page
  - [ ] product page adjustment
  - [ ] submit payment
    - [x] db table
    - [ ] Cash Payment: Enter amount and date
    - [ ] Goods Payment: Enter Weight, Quality, Rate, and Total Amount
- [ ] received product
- [ ] paid / unpaid transactions
- [ ] action log on dashboard
  - [ ] activity log
  - [ ] auto reload
  - [ ] sound on updates
  - [ ] outstanding payments per retailer
- [ ] pg full text search
- [ ] make sure only either supplier or retailer is specified
- [ ] custom fields
- [ ] limit number of users and products per hr
- [ ] remove product before received?
- [ ] highlight selected menu?
- [ ] use slider for quality?
- [ ] validate and print errors for login/registration forms
- [ ] use details for errors response, not message
- [ ] validate login/register input inside js
- [ ] datetime -> date? (product and payment)

Other:

- [ ] Security
  - [ ] DB backups
  - [ ] sentry
- [ ] UI improvements
  - [ ] icon
  - [ ] mobile
  - [ ] keep the tab that was selected last time
  - [ ] pick up color scheme / theme switch
  - [ ] show errors under fields in the form
- [ ] Company / Legal
- [ ] Landing page
- [ ] download products as csv
- [ ] Products
  - [ ] ordering
  - [ ] filtering
- [ ] disable/reenable staff
- [ ] add message about 2 moths trial free
- [ ] terms of use

Questions:
- validation of product fields?
- Dashboard: not received, paid, confirmed, outstanding per retailer?
- Dashboard: updates for products
- What is Date in product?
- new domain?
- icons in forms
- separate page for new product instead of modal?
- sent -> (canceled, received) -> paid -> payment confirmed
- show not paid, confirmed, etc.
- setup CI tests on github
- do we need a photo for payment?
- how the store id looks like?
- Write terms of use?
- Landing page
