import requests
from bs4 import BeautifulSoup

gstins="21ABCDE1234F1ZY"

filename = "result.html"
URL = "https://my.gstzen.in/p/free-gstin-validator/"


def get_html(URL,gstins):
    #################
    client = requests.session()
    client.get(URL)

    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    else:
        # older versions
        csrftoken = client.cookies['csrf']
    params = dict(text=gstins, csrfmiddlewaretoken=csrftoken, next='/')
    r = client.post(URL, data=params, headers=dict(Referer=URL))
    if r.status_code != 200:
        print("Status code is'nt 200...")
    return r.text
#############

# with open(filename,"w+") as f:
#     f.write(r.text)

def parse_html(html_doc):
    # parse the result 
    # classnames = "table table-striped table-bordered table-sm sortable"
    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.table 

    result = []
    for row in table.find_all("tr")[1:]:
        data = []
        for col in row.find_all("td"):
            if "fa-times-circle" in str(col):
                text = "False"
            elif "fa-check-circle" in str(col):
                text = "True"
            else:
                text = col.get_text()
            
            data.append(text)
        result.append(data)
    return result

print(parse_html(get_html(URL,gstins)))