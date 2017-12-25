import json
import requests
from app_crawler.models import zhengxin91_content
from app_crawler.models import zhengxin91_crawler_log
from app_crawler.models import zhengxin91_ori_data
from app_crawler.storage.zhengxin91.manager import Manager
from crawler.settings import logger


class ZhengXin91(Manager):
    def main(self,data:dict)->bool:
        c = zhengxin91_crawler_log()
        try:
            self.verify_query(data,c)
            if data[self.FLAG] == self.BSDFLAG and self.not_expire(zhengxin91_content,data):
                try:
                    self.update_existed(data)
                    self.update_succLog(c)
                    logger.info("the data has been in database,update ctime")
                    return True
                except:
                    self.update_failLog(c)
                    raise Exception(self.Error.EXISTED_FAIL_HINT)
            resp = self.request(data,c)
            logger.info("this is receive response")
            logger.info(resp)
            parsed = self.parse(resp,c)
            logger.info("this is parsed")
            logger.info(self.json_marshal(parsed[1]))
            self.storage(parsed,data,c)
            self.save_log(self.RIGHT,c)
            return True
        except:
            self.save_log(self.WRONG, c)
            logger.error("query_storage error",exc_info=True)
            return False

    def verify_query(self,data:dict,c):
        try:
            assert type(data)==dict
            assert data[self.UserInfo.REC_NAME] != ""
            assert data[self.UserInfo.REC_IDCARD] != ""
            assert data[self.FLAG] != ""
            c.verify_res = self.RIGHT
            c.idcard = data.get(self.UserInfo.REC_IDCARD, "")
            c.name = data.get(self.UserInfo.REC_NAME, "")
            logger.info("verify query success")
        except:
            c.verify_res = self.WRONG
            c.note = self.Error.ILLEAGL_NOTE
            logger.error("verify error",exc_info=True)
            raise Exception(self.Error.ILLEAGL_NOTE)

    def update_existed(self,hm_data):
        zx = zhengxin91_content
        trx_no = zx.objects.using(self.HMDB).filter(idcard=hm_data[self.UserInfo.REC_IDCARD]).order_by("-id")[:1][0].trx_no
        zx.objects.using(self.HMDB).filter(trx_no=trx_no).update(ctime=self.now,ctime_stamp=self.now_stamp)
        parsed = (self.Error.EXISTED_ERROR,self.Error.EXISTED_HINT)
        self._store_ori(parsed,hm_data)


    def request(self,data,c)->str:
        try:
            user_data = self._encode_query(data)
            resp = requests.post(self.Authentication.QUERY_URL, data=user_data)
            c.request_res = self.RIGHT
            logger.info("request success")
            return resp.text
        except:
            c.request_res = self.WRONG
            tag = "request error"
            logger.error(tag,exc_info=True)
            raise Exception(tag)

    def _encode_query(self,data:dict)->str:
        post_data = {
            self.UserInfo.REC_NAME:data[self.UserInfo.REC_NAME],
            self.UserInfo.REC_IDCARD:data[self.UserInfo.REC_IDCARD],
        }
        to_base64 = self.zhengxin_encode(post_data)
        body = f"01|{self.Authentication.COMPANY_CODE}|01|{self.Code.QUERY_MSG}" \
               f"|01|01|{to_base64}|||{self.Authentication.SIGNATURE}"
        return body

    def parse(self,resp:str,c)->tuple:
        try:
            status_code,extracted = self._extract(resp)
            py_obj = self._decode(extracted)
            c.parse_res = self.RIGHT
            return status_code,py_obj
        except:
            logger.error("parse error",exc_info=True)
            c.parse_res = self.WRONG
            raise Exception("parse error")

    def _extract(self,resp:str)->tuple:
        to_list = resp.split("|")
        assert len(to_list) == self.ZX_LENGTH
        if to_list[3] == "":
            status_code = to_list[-3]
            body = to_list[-2]
        else:
            status_code = to_list[3]
            body = to_list[6]
        return status_code,body

    def _decode(self,extracted:str)->"dict/str":
        de_res = {}
        try:
            de_res = self.zhengxin_decode(extracted)
        except:
            logger.error("_decode",exc_info = True)
        return de_res

    def storage(self,parsed:tuple,data:dict,c):
        try:
            self._store_ori(parsed,data)
            code, concrete = parsed
            assert code == self.Code.SYNCHRONOUS_INTERFACE_CODE
            flag = data[self.FLAG]
            if flag == self.BSDFLAG:
                self._store_bsd(parsed,data)
            elif flag == self.SSDFLAG:
                self._store_ssd(parsed,data)
            else:
                raise Exception(f"Unexpected flag {flag}")
            c.insert_res = self.RIGHT
            logger.info("storage success")
        except:
            logger.error("storage error",exc_info=True)
            c.insert_res = self.WRONG
            raise Exception("storage error")

    def _store_ori(self,parsed:tuple,data:dict):
        assert len(parsed) == 2
        zx = zhengxin91_ori_data()
        zx.name = data[self.UserInfo.REC_NAME]
        zx.idcard = data[self.UserInfo.REC_IDCARD]
        zx.flag = data[self.FLAG]
        zx.status_code = parsed[0]
        zx.ori_data = json.dumps(parsed[1])
        zx.save()

    def _store_bsd(self,parsed:tuple,data:dict):
        code,concrete = parsed
        zx = zhengxin91_content()
        zx.status_code = code
        zx.name = data[self.UserInfo.REC_NAME]
        zx.idcard = data[self.UserInfo.REC_IDCARD]
        zx.ctime_stamp = self.now_stamp
        if isinstance(concrete, str):
            zx.err_msg = concrete
            zx.save(using=self.HMDB)
            raise Exception("Interface return symolic error of code")
        elif isinstance(concrete, dict):
            loanInfos = concrete["loanInfos"]
            zx_list = []
            core = self.ZhengXin91LoanCoreInfo
            for loan in loanInfos:
                zx_list.append(
                    zhengxin91_content(
                        status_code = 0 if code == 0 else code,
                        name = data[self.UserInfo.REC_NAME],
                        idcard = data[self.UserInfo.REC_IDCARD],
                        ctime_stamp = self.now_stamp,
                        trx_no = concrete["trxNo"],
                        borrow_type = loan.get(core.BORROWSTATE,0),
                        borrow_status = loan.get(core.BORROWSTATE,0),
                        borrow_amount = loan.get(core.BORROWAMOUNT,0),
                        contract_data = loan.get(core.CONTRACTDATE,""),
                        loan_period = loan.get(core.LOANPERIOD,0),
                        repay_state = loan.get(core.REPAYSTATE,0),
                        arrears_amount = loan.get(core.ARREARSAMOUNT,0),
                        company_code = loan.get(core.COMPANYCODE,""),
                    )
                )
            if len(loanInfos) == 0:
                logger.info("the message of zhengxin91 responsed is empty")
                zx_list.append(
                    zhengxin91_content(
                        status_code=0 if code == 0 else code,
                        name=data[self.UserInfo.REC_NAME],
                        idcard=data[self.UserInfo.REC_IDCARD],
                        ctime_stamp=self.now_stamp,
                        trx_no=concrete["trxNo"],
                        borrow_type= 0,
                        borrow_status= 0,
                        borrow_amount= 0,
                        contract_data= "",
                        loan_period=0,
                        repay_state=0,
                        arrears_amount=0,
                        company_code="",
                    )
                )
            zhengxin91_content.objects.using(self.HMDB).bulk_create(zx_list)
        else:
            print(self.now,concrete)
            print(self.now,type(concrete))
            raise Exception("Unexpected concrete struct")
    def _store_ssd(self,parsed:tuple,data:dict):
        raise Exception("not allow saved in ssd;this function is developing!")


if __name__ == "__main__":
    zx91 = ZhengXin91()
    data = {'flag':'HM/SSD','realName': '陈水金', 'idCard': '350424198301082038'}
   



