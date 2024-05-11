import requests
from bs4 import BeautifulSoup

gstins="21ABCDE1234F1ZY"
class Gstin:
    def __init__(self,gst):
        self.gst = gst 
        self.check_gst(gst)

    def isvalid(self):
        if self.data[-1] == 'True':
            return True 
        return False
    
    def get_name(self):
        if self.isvalid():
            return self.data[2]
        elif self.data == "No internet":
            return self.data
    
    def get_gstno(self):
        if self.isvalid():
            return self.data[1]

    def get_html(self,gstins):
        URL = "https://my.gstzen.in/p/free-gstin-validator/"
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

    def get_results(self,gstins):
        html_doc = self.get_html(gstins)
        # parse the result 
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = soup.table 
        result = []
        for row in table.find_all("tr")[1:]:
            data = []
            for col in row.find_all("td"):
                if "fa-times-circle" in str(col): text = "False"
                elif "fa-check-circle" in str(col): text = "True"
                else: text = col.get_text()            
                data.append(text)
            result.append(data)
        return result

    def check_gst(self,gst):
        try:
            data = (self.get_results(gst))
        except requests.exceptions.ConnectionError:
            print("Make Sure you are connected to the internet")
            data = ["No internet"]
        except:
            raise
        if data:
            self.data = data[0]
        else:
            self.data = []
        return data
    
    def __str__(self):
        return self.get_gstno()

if __name__ == '__main__':
    gstno = "21AFYPA4772J1Z7"
    obj = Gstin(gstno)
    print(obj.get_name())