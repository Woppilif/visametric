import requests 


class VisaMetric:

    def __init__(self,pass_id,user_id):
        self.pass_id = int(pass_id)
        self.user_id = int(user_id)

    def send_response(self,response):
        response = response.text.split('#')
        if len(response) < 4:
            return False
        if response[0] == '1':
            return response[1], ' '.join((response[2],response[3]))
        return False


    def get_info(self):
        r = requests.get('https://www.visametric.com/Germany/ru/app/17/{0}/{1}'.format(self.pass_id,self.user_id))

        if r.status_code == 200:
            return self.send_response(r)
        else:
            return False


visa  = VisaMetric(751223129,17094643)
print(visa.get_info())