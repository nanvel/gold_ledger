# Plan

Next:
- [x] remove staging
  - [x] remove files in the s3 bucket!
  - [x] remove dev from pulumi
- [x] fix transaction error
- [ ] retailers and suppliers pages
  - [x] db (connection, invite)
  - [x] invites repo 
  - [x] link view
    - [x] link api 
  - [ ] UI
    - [x] generate url
    - [x] show QR + url + message
    - [ ] copy url button
    - [ ] show retailers/suppliers
    - [ ] the same thing for retailer
    - [ ] add to navbar
    - [ ] refactor recents
  - [ ] update migration to add connections
  - [ ] limit searches
  - [ ] add retailer/supplier
- [ ] download products/payments/activities csv
- [ ] do not allow payment if there is no products yet
- [ ] connect to retailer/supplier, retailer/supplier list
- [ ] description in index.html
- [ ] landing page
  - [ ] how to use the software
- [ ] recaptcha on registration
- [ ] note for product
- [ ] remove rate when fine is selected

Security:
- [ ] change secret, change db password, backup secrets
- [ ] backup secrets and keys
- [ ] encode secret and move it to supervisor
- [ ] storage options?
  - [ ] increase disk size?
- [ ] ensure debug mode is disable in tastypie, no api exposure
- [ ] limit number of users and products per hr
- [ ] db replication
- [ ] traffic monitoring (waf?)
  - block IPs
- [ ] limit image uploads
- [ ] registration by invite (QR code?)
- [ ] confirm email
- [ ] AWS waf?

UI:
- [ ] improve recent on small screen
- [ ] card view for payments?
- [ ] note for product
- [ ] navbar glass?

Pages:
- [ ] terms of use
- [ ] prices
- [ ] support
- [ ] docs pages: What is Gold Ledger, Terms of use, prices
- [ ] customer support

Refactor:
- [ ] server folder
  - [ ] database owner to gold_ledger
  - [ ] README
- [ ] image input component
- [ ] tablist component

Other:
- [ ] docs.goldledger.in?
- [ ] logo on login page
- [ ] record IPs for activities
- [ ] pg full text search
- [ ] custom fields
- [ ] highlight selected menu?
- [ ] send email on each transaction
- [ ] Company / Legal
- [ ] payments https://onboarding.payu.in/
- [ ] Landing page
- [ ] disable/reenable staff
- [ ] auto reload activities
  - [ ] sound on updates
- [ ] referral program
- [ ] setup CI tests on github
- [ ] do we need a photo for payment?
- [ ] translate to India language
- [ ] sending messages

Company:
- LLP
- neutral name (not gold ledger)
- Open AWS account
- Open PayU account
- Open Google account (support@goldledger.com)
