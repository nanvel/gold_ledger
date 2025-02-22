# Plan

Next:
- [x] remove staging
  - [x] remove files in the s3 bucket!
  - [x] remove dev from pulumi
- [x] fix transaction error
- [x] retailers and suppliers pages
  - [x] db (connection, invite)
  - [x] invites repo 
  - [x] link view
    - [x] link api 
  - [x] UI
    - [x] generate url
    - [x] show QR + url + message
    - [x] copy url button
    - [x] check connection when creating product/payment
    - [x] show retailers/suppliers
      - [x] api
    - [x] retailers table
    - [x] the same thing for retailer
    - [x] add to navbar
  - [x] update migration to add connections
  - [x] limit searches
  - [x] refactor recents
    - [x] load all initially 
  - [x] "Add suppliers/retailers at ..."
- [x] download products/payments/activities csv
- [ ] record who accepted the invite
- [ ] do not allow payment if there is no products yet
- [ ] refactor suppliers/retailer loading, try to use v-show instead
- [ ] landing page
  - [x] how to use the software
  - [ ] https://daisyui.lemonsqueezy.com/checkout
  - [ ] description in index.html
  - [ ] Terms of use
- [ ] recaptcha on registration
- [ ] note for product
- [ ] remove rate when fine is selected
- [ ] guide around the app
- [ ] default value for due date - 1 week
- [ ] support email?
  - [ ] https://www.spaceship.com/business-email/
- [ ] image when sharing in index.html

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
- [x] default theme - light 

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
- [ ] apps
  - [ ] progressive web app
  - [ ] ios
  - [ ] android
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
