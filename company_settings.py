import datetime


#Name of the Company
COMPANY_NAME = "SAAD TECHNOLOGIES"

#Abbreviation of the Company 
COMPANY_ABBR = "ST"

#How the Invoices are to be written
INVOICE_FORMAT = "{company}/{invoice_no}/{year}"

def get_invoice(last_invoice_no):
    now = datetime.datetime.now()
    if now.month >= 4:
        # Financial Year Changed
        start = str(now.year)[-2:]
        end = str(now.year+1)[-2:]
    else:
        start = str(now.year-1)[-2:]
        end = str(now.year)[-2:]
    year = ""
    invoice_no = 0 # given '0' if invoice no is not updated i can identify that
    for i in last_invoice_no.split("/"):
        if "-" in i:
            year = i
        elif i.isdigit():
            invoice_no = int(i)+1
    if year and year!=f"{start}-{end}":
        invoice_no=1
    return INVOICE_FORMAT.format(company=COMPANY_ABBR,invoice_no=str(invoice_no).rjust(4,'0'),year=f"{start}-{end}")
