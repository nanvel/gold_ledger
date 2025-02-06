# Plan

Payments summary:
- [x] study messages
- [x] service for due
- [x] due payments
- [x] swap selector and table view in products
- [x] refactor logic, cache
  - [x] refactor service
  - [x] cache db
- [x] move service to container
- [x] cache repo
  - [x] model
- [x] use the use case in the message bus (for confirmed)
- [x] use case for recalculate for all
- [x] refactor api

Payments UI:
- [x] disallow past due dates
- [x] rename to balance sheet
- [x] filter by id/name
- [ ] colors for overdue / amount
- [ ] summary
- [ ] show overdue on home?
- [ ] show pending payments/products on main?
- [ ] rename handler
- [ ] version for meStore

UI more:
- [ ] new payment/product right navbar
  - [x] button
  - [ ] refresh products/payments/activities
- [ ] show pay n amount to by date
- [ ] note for payment
- [ ] products/payments waiting for approval on dashboard

Deployment:
- [ ] connect sentry
- [ ] encode secrets
- [ ] refactor server folder
  - [ ] storage options? 
- [ ] use the new domain
  - [ ] docs.goldledger.in?
- [ ] Mumbai region
- [ ] ensure debug mode is disable in tastypie, no api exposure

Other:
- [ ] cleanup plan
- [ ] compute due payments / products
- [ ] overdue payments on the product page? (paid/not paid)
- [ ] refine cards ui
- [ ] refine tables ui
- [ ] refine products page
- [ ] refine payments page
- [ ] refine product page
- [ ] refine payment page
- [ ] color circles for status
- [ ] show retailer and supplier in payments and products
- [ ] improve recent on small screen
- [ ] cancel payment / product
- [ ] due payments page
- [ ] message bus
  - [ ] record IPs for activities
- [ ] move business logic into models
  - [ ] validate user has either supplier or retailer id
  - [ ] set confirmed / rejected
- [ ] reset -> set password
- [ ] retailer page
  - [ ] make sure we show ids 
  - [ ] only show for suppliers
- [ ] products filtering
- [ ] payments filtering
- [ ] supplier page
  - [ ] only show for retailers
- [ ] make sure showing all data
  - [ ] show activities for product
  - [ ] show activities for payment
- [ ] statuses for payment
  - [ ] color circles for status
  - [ ] compute status in model
- [ ] improve cards and tables display
- [ ] UI improvements
  - [ ] show empty list placeholder (don't show table/cards placeholder)
  - [ ] image input
  - [ ] make navbar sticky
  - [ ] add ruppy, gramm
- [ ] received product
- [ ] paid / unpaid transactions
- [ ] make sure store is visible after login
- [ ] pg full text search
- [ ] make sure only either supplier or retailer is specified
- [ ] custom fields
- [ ] limit number of users and products per hr
- [ ] highlight selected menu?
- [ ] validate login/register input inside js
- [ ] add more input components, label - div
- [ ] autocalculate amount for goods payment?
- [ ] use message bus for activities
- [ ] cancel transaction
- [ ] try adding image from phone
- [ ] send email on each trasaction
  - [ ] message bus
- [ ] incremental log on dynamodb
- [ ] tablist component
- [ ] email updates
- [ ] Mumbai region
- [ ] filter by status (products and payments)

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
- [ ] auto reload activities
  - [ ] sound on updates
- [ ] outstanding payments per retailer
- [ ] docs pages: What is Gold Ledger, Terms of use, prices
- [ ] move activities to DDB
- [ ] pg replication
- [ ] card view for payments

Security:
- limit number of registrations
- limit images upload
- block IPs
- confirm email
- sending reports via email
- download records
- db replication

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
- support link (password loss, etc.)

Enhancement:
- [ ] order table values by clicking on table header
