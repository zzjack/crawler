import json
import base64


encoded_exmaple = '01|SRV1A4G0000000001|01|3001|01|01|eyJyZWFsTmFtZSI6IuWQtOaFleaBqSIs' \
       'ImlkQ2FyZCI6IjMyMDIwMjE5NzkwNDAzNDAxWCIsImNvbXBhbnlDb2RlIjoiUDJQQlZDRDAw' \
       'MDAxMDAwMDEifQ==|||'

class accepted_maker():
    module1 = "01|SRV1A4G0000000001|01|3001|01|01|"
    module2 = "|||"
    def maker(self,rcv:dict):
        jsoned = json.dumps(rcv).encode()
        res = base64.b64encode(jsoned).decode()
        module = self.module1 + res + self.module2
        return module


shared_example = "01|P2PHJ9D0000100108|01|4001|01|01|eyJsb2FuX2luZm9zIjogW3siYm9" \
                 "ycm93VHlwZSI6IDEsICJib3Jyb3dTdGF0ZSI6IDAsICJib3Jyb3dBbW91bnQiOiAwL" \
                 "CAiY29udHJhY3REYXRlIjogIjAiLCAibG9hblBlcmlvZCI6IDAsICJyZXBheVN0YXRlIjogM" \
                 "CwgImFycmVhcnNBbW91bnQiOiAwLCAiY29tcGFueUNvZGUiOiAiUDJQSEo5RDAwMDAxMDAxMDgif" \
                 "V19|0000||"

def shared_decode(rcv:str):
    splited = rcv.split("|")
    s = base64.b64decode(splited[6]).decode()
    print(s)


if __name__ == "__main__":
    # decode response value
    # te = '01|P2PHJ9D0000100108|01|4001|01|01|eyJsb2FuX2luZm9zIjogW3siYm9ycm93VHlwZSI6IDEsICJib3Jyb3dTdGF0ZSI6IDAsICJib3Jyb3dBbW91bnQiOiAwLCAiY29udHJhY3REYXRlIjogIjAiLCAibG9hblBlcmlvZCI6IDAsICJyZXBheVN0YXRlIjogMCwgImFycmVhcnNBbW91bnQiOiAwLCAiY29tcGFueUNvZGUiOiAiUDJQSEo5RDAwMDAxMDAxMDgifV19|0000||'
    # shared_decode(shared_example)

    # encode request value
    a = accepted_maker()
    rcv = {
        "companyCode": "SRV1A4G0000000001",
        "realName": "刘海涛",
        "idCard": "530181199603153937"
    }
    res = a.maker(rcv)
    print(res)
