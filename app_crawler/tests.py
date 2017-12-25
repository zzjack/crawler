import base64
import json
import csv
from collections import namedtuple

a = "01|SRV1A4G0000000001|01|3001|01|01|eyJyZWFsTmFtZSI6IuWQtOaFleaBqSIsImlkQ2FyZCI6IjMyMDIwMjE5NzkwNDAzNDAxWCIsImNvbXBhbnlDb2RlIjoiUDJQQlZDRDAwMDAxMDAwMDEifQ==|||"
to_list = a.split("|")

b = "eyJsb2FuSW5mb3MiOlt7ImJvcnJvd1R5cGUiOjEsImJvcnJvd1N0YXRlIjoyLCJib3Jyb3dBbW91bnQiOjMsImNvbnRyYWN0RGF0ZSI6IjIwMTItMDgtMDEiLCJsb2FuUGVyaW9kIjoyNCwicmVwYXlTdGF0ZSI6NywiYXJyZWFyc0Ftb3VudCI6MC4wLCJjb21wYW55Q29kZSI6IlAyUDRISkswMDAwMTAwMDEwIn0seyJib3Jyb3dUeXBlIjoxLCJib3Jyb3dTdGF0ZSI6MiwiYm9ycm93QW1vdW50IjozLCJjb250cmFjdERhdGUiOiIyMDEyLTA4LTAxIiwibG9hblBlcmlvZCI6MjQsInJlcGF5U3RhdGUiOjcsImFycmVhcnNBbW91bnQiOjAuMCwiY29tcGFueUNvZGUiOiJQMlA0SEpLMDAwMDEwMDAxMCJ9XX0="

temp = {
    "loanInfos":[
        {
            "borrowType":1,
            "borrowState":2,
            "borrowAmount":3,
            "contractDate":"2012-08-01",
            "loanPeriod":24,
            "repayState":7,
            "arrearsAmount":0,
            "companyCode":"P2P4HJK0000100010"
        },
        {
            "borrowType":1,
            "borrowState":2,
            "borrowAmount":3,
            "contractDate":"2012-08-01",
            "loanPeriod":24,
            "repayState":7,
            "arrearsAmount":0,
            "companyCode":"P2P4HJK0000100010"
        }
    ]
}


def json_ummarshal(rcv: str) -> "pyobj":
    assert isinstance(rcv, str) == True
    assert len(rcv) > 0
    return json.loads(rcv)


def json_marshal(rcv: dict) -> str:
    assert isinstance(rcv, dict)
    return json.dumps(rcv)

def zhengxin_encode(data: dict) -> str:
    marshaled = json_marshal(data)
    encoded = base64.b64encode(marshaled).decode()
    return encoded


def zhengxin_decode(data: str) -> "obj":
    return json_ummarshal(base64.b64decode(data).decode())

class ww():
    a = 1

def a():
    for i in []:
        print(i["hello"])

def w():
    a = {"m":123}
    print(a.m)

if __name__ == "__main__":
    a()
