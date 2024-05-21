# Todo

- Add support of Purchase Invoice - (*Working*)
- Add Security measures
- Add Test cases
- Fix all items IGST from 0% to required values
<!-- - Fix Navbar on Shrinking window
  -  The problem is in main wrapper
  - The main wrapper should be present outside the header, sidebar and footer part.  it will wrap everything -->
- Remove Profile of User
- Remove Inbox of user
- Remove ID column from each table
- Implement check on every invoice
  - Invoice no is Serial Wise
  - User can only **edit** invoice and **cancel** invoice but they **cannot delete** it.
- Fix Dashboard
- Fix `Welcome admin` to `Welcome {name}`
- Allow login with username (dangerous for security)
<hr />

### *Invoice (design)*
- Fix trxn addon
- fix cgst

### *Edit Invoice*
<!-- - Make edit invoice part separately (Completely Separate) -->
- No reset button on edit
### *Sale Invoice*
<!-- - Add preview Invoice - *already working* -->
  <!-- - Decide format of invoice -->
  <!-- - Design in HTML/CSS (probably) -->
  <!-- - integrate it with django -->
  <!-- - Ability to convert it into pdf file and save locally  -->
<!-- - Add print Invoice
  - simple Browser printer (maybe we can use this to convert to pdf) -->
<!-- - Fix Delete trxn addon button  - After refreshing page, delete button stop working correctly - Fixed -->
<!-- - Add edit button to trxn addon - I think its better not to add it. -->
<!-- - Change sessionStorage to localStorage -->
<!-- - Remove all console.log methods -->
<!-- - Make all inputs in trxn addon disabled (to prevent miscalculation) - The name input can be left enabled -->
<!-- - Put a loading screen during save invoice async -->
<!-- - Show error in the modal dialog after save_invoice press - done -->
<!-- - Add State to Shipping detail in invoice async save (backend) -->
<!-- - Fix Save Invoice On change shipping address -->
- Update Customer balance, item quantities etc in save_invoice in views(backend)
  - Do it from pre save and post save of models
  - Do Same for delete invoice, transactions, edit invoice etc
- Remove test from vendor_views
<!-- - Fix the modal CSS that are affected because of iframe. -->
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
<!-- - Add URL to Preview/print Button of each list item (Take it from `add_invoice.html`) -->
### *Purchase Invoice*
- Write complete code similar to Sale invoice
  - Find a way to async save file
  - Rest of code must be similar to sale invoice (Helps in good UI)
- **Suggestion**: do we need change shipping addr??
- Add edit purchase invoice
### *Sale return*
- Add format for printing sale returns
<!-- - Remove redeem options -->
  <!-- - remove the column status in view sale return -->
  <!-- - remove the field status in edit sale return -->
  <!-- - remove redeem status from models.py -->
<!-- - 'update on post save' and delete code from views -->
  <!-- - remove it from views.py -->
  <!-- - add a signal on signals.py -->
### *Purchase return*
<!-- - Remove redeem options -->
  <!-- - remove the column status in view purchase return -->
  <!-- - remove the field status in edit purchase return -->
  <!-- - remove redeem status from models.py -->
- Change the name from VendorCreditNote to PurchaseReturn (stfart from models.py and change them in vendor views.py too)
- 'update on post save' and delete code from views
  - remove it from views.py
  - add a signal on signals.py
<!-- ### *Customer / Vendor* -->
<!-- - Add Checking for valid GST (Automatic check internet if possible) -->
<!-- - Add (Automatic check internet gst details) -->  
  <!-- - `https://github.com/pranav7712/OFFICE_AUTOMATION/blob/main/GSTIN_VALIDATOR_PYTHON.py#L66`
  - POST request to `https://my.gstzen.in/p/free-gstin-validator/?`
  - To pass CSRF token : `https://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests` -->
  <!-- - Functions made, just needed to be implemented -->
<!-- - Add Checking for valid PAN card (Automatic check internet if possible) -->
<!-- - Add edit option inside the view single vendor -->
<!-- - Fix website url in vendors details -->
## *Google drive Support*
- Add support for google drive operations where the whole database(*db.sqlite3*) gets updated timely whenever internet gets connected. Users can change the time according to their will. 


<hr />

<!-- # Reports --> 
<!-- - Fix navbar link -->

# Addons
- Short description of each tab on inside modal with button written "details" on it. with info part

# Need of Internet
<!-- - Check post_save syntax -->
<!-- - do the gst_check part -->
<!-- - Find a way to async save file for Purchase invoice -->
- Fix the media settings