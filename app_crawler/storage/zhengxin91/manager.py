import datetime
import time
import json
import base64
from collections import namedtuple
from crawler.settings import logger


class Manager:
    FLAG = "flag"
    SSDFLAG = "SSD"
    BSDFLAG = "HM"
    HMDB = "helpMe"
    JKWEB = "helpMe_jkweb"
    DEFAULT_LIMIT = 7
    RIGHT = "1"
    WRONG = "0"
    ZX_LENGTH = 10
    COMPANYCODE = "companyCode"
    NOTEXIST = 0
    EXISTED = 1
    now = datetime.datetime.now()
    now_stamp = int(time.time())


    class UserInfo:
        REC_NAME = "realName"
        REC_IDCARD = "idCard"
        COMPANYCODE = "companyCode"


    class Error:
        EXISTED_HINT = "crawling user exsited"
        EXISTED_ERROR = "existed"
        EXISTED_SUCC_HINT = "exsited data is not expire;ctime was updated only"
        EXISTED_FAIL_HINT = "exsited data is not expire;It failed in update"
        ILLEAGL_NOTE = "receive data is illegal"



    class Authentication:
        COMPANY_CODE = "P2P31DSDLNV5218ZA"
        SIGNATURE = "4D60256EB7154126B6276F5557DCC381"
        QUERY_URL = "http://service.91zhengxin.com/jyzx/zxservice.do"


    class Code:
        SHARE_EXISTED = "shared"
        QUERY_MSG = "1003"
        SYNCHRONOUS_INTERFACE_CODE = "2003"
        SHARE_REQ_CODE = "3001"
        SHARE_RESP_NUM = "4001"

    class ZhengXin91LoanCoreInfo:
        BORROWTYPE = "borrowType"
        BORROWSTATE = "borrowState"
        BORROWAMOUNT = "borrowAmount"
        CONTRACTDATE = "contractDate"
        LOANPERIOD = "loanPeriod"
        REPAYSTATE = "repayState"
        ARREARSAMOUNT = "arrearsAmount"
        COMPANYCODE = "companyCode"

    def step_return(self):
        S = namedtuple("step","val res")
        return S

    def zhengxin_encode(self,data:dict)->str:
        marshaled = self.json_marshal(data).encode()
        encoded = base64.b64encode(marshaled).decode()
        return encoded

    def zhengxin_decode(self,data:str)->"obj":
        return self.json_ummarshal(base64.b64decode(data).decode())

    def json_ummarshal(self,rcv:str)->"pyobj":
        assert isinstance(rcv,str) == True
        assert len(rcv) > 0
        return json.loads(rcv)

    def json_marshal(self,rcv:dict)->str:
        assert isinstance(rcv,dict)
        return json.dumps(rcv)

    def notEmptyDict(self,adict:dict)->bool:
        try:
            assert isinstance(adict,dict)
            for k in adict:
                assert adict[k] != ""
            return True
        except:
            print("assert dict",adict)
            logger.error("not Empty dict",exc_info = True)
            return False

    def not_expire(self,table:"table object",userInfo:dict)->bool:
        zx = table
        idcard = userInfo[self.UserInfo.REC_IDCARD]
        if "ZhengXin" in table.__name__:
            queryRes = zx.objects.filter(idcard=idcard).order_by("id")
        else:
            queryRes = zx.objects.using(self.HMDB).filter(idcard=idcard).order_by("id")
        if len(queryRes) == 0:
            return False
        else:
            cln = queryRes[:1][0]
            return self._calc_expire(cln.ctime_stamp)

    def _calc_expire (self,ctime_stamp:int,limit = DEFAULT_LIMIT)->bool:
        limit_sec = 24 * 3600 * limit
        if ctime_stamp + limit_sec > self.now_stamp:
            return True
        else:
            return False

    def update_succLog(self,table:"table object"):
        table.note = self.Error.EXISTED_SUCC_HINT
        table.status = self.RIGHT
        logger.info(self.Error.EXISTED_SUCC_HINT)
        table.save()

    def update_failLog(self,table:"table object"):
        table.note = self.Error.EXISTED_FAIL_HINT
        table.status = self.WRONG
        logger.info(self.Error.EXISTED_FAIL_HINT)

    def save_log(self,flag,table):
        status = "successfully"
        if flag == self.RIGHT:
            table.status = self.RIGHT
        else:
            table.status = self.WRONG
            status = "un" + status
        table.save()
        logger.info(f"{table.__class__.__name__} {status} saved")

if __name__ == "__main__":
    print(time.time(),int(time.time()))
