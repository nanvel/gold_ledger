# Plan

Payments summary:
- [x] study messages
- [ ] service for due
- [ ] due payments

DDB for activities:
- [ ] message bus
- [ ] ddb table
- [ ] refactor activities repo

Deployment:
- [ ] refactor server folder
- [ ] use the new domain
- [ ] Mumbai region

Other:
- [ ] use slug instead of label in payment type
- [ ] order table values by clicking on table header
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
