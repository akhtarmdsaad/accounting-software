# Todo

- Add support of Purchase Invoice
- Add Security measures
- Add Test cases
- Fix all items IGST from 0% to required values
- Fix Navbar on Shrinking window
- Profile of User
- Inbox of user
- Remove ID column from each table
- Implement check on every invoice
- Correct the CSS during shrinking window
- Fix Dashboard
<hr />

### *Edit Invoice*
- Add `edit_invoice.html` to templates
### *Sale Invoice*
- Add preview Invoice - *already working*
  <!-- - Decide format of invoice -->
  <!-- - Design in HTML/CSS (probably) -->
  - integrate it with django
  - Ability to convert it into pdf file and save locally 
- Add print Invoice
  - simple Browser printer (maybe we can use this to convert to pdf)
<!-- - Fix Delete trxn addon button  - After refreshing page, delete button stop working correctly - Fixed -->
<!-- - Add edit button to trxn addon - I think its better not to add it. -->
<!-- - Change sessionStorage to localStorage -->
<!-- - Remove all console.log methods -->
<!-- - Make all inputs in trxn addon disabled (to prevent miscalculation) - The name input can be left enabled -->
<!-- - Put a loading screen during save invoice async -->
<!-- - Show error in the modal dialog after save_invoice press - done -->
- Add State to Shipping detail in invoice async save (backend)
- Update Customer balance, item quantities etc in save_invoice in views(backend)
  - Do it from pre save and post save of models
  - Do Same for delete invoice, transactions, edit invoice etc
- Remove test from vendor_views
<!-- - Add CGST to "tax percent" -> "CGST tax percent" in Add Item modal and in the table. -->
- **Take Suggestion**: Reset data after click of Add Button.  
<!-- - Handle the Async in backend and return appropriate statuses - *already working* -->
### *View Invoice*
<!-- - Enable Search Invoice no -->
- **Suggestions**: Is dual pagination good? 
<!-- - Fix Search Invoice no at last scroll -->
<!-- - Edit invoices URL takes to Customer update page
- Delete url takes to customer page -->
<!-- - Add Preview/print Button to each list item  -->
- Add URL to Preview/print Button of each list item (Take it from `add_invoice.html`)
### *Purchase Invoice*
- Write complete code similar to Sale invoice
  - Find a way to async save file
  - Rest of code must be similar to sale invoice (Helps in good UI)
### *Sale return*
- Remove redeem options
### *Purchase return*
- Remove redeem options

### *Customer / Vendor*
<!-- - Add Checking for valid GST (Automatic check internet if possible) -->
- Add (Automatic check internet gst details)
<!-- - Add Checking for valid PAN card (Automatic check internet if possible) -->
- Add edit option inside the view single customer
- Fix website url in vendors details
<hr />

# Reports 
- Fix navbar link

# Addons
- Short description of each tab on inside modal with button written "details" on it. with info part