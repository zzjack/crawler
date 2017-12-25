from collections import namedtuple
from app_crawler.storage.zhengxin91.manager import Manager
from app_crawler.models import ZhengXin91ShareLog
from app_crawler.models import ZhengXin91ShareOriData
from app_crawler.models import JkLoanApply
from app_crawler.models import JkUserLoanRecord
from crawler.settings import logger


class ZhengXin91Shared(Manager):
    def main(self,rcv:str)->(str,bool):
        log_db = ZhengXin91ShareLog()
        try:
            self.verify(rcv,log_db)
            parsed = self.parse(rcv,log_db)
            self.verify_meanful_rcv(parsed, log_db)

            if self.not_expire(ZhengXin91ShareOriData,parsed):
                try:
                    extracted = self.extract_not_expire(parsed)
                    log_db.note = "response from cache, succeed!"
                    self.save_log(self.RIGHT,log_db)
                    logger.info(log_db.note)
                    return extracted,True
                except:
                    log_db.note = "response from cache, failed!"
                    self.save_log(self.WRONG,log_db)
                    logger.info(log_db.note)
                    raise Exception(self.Error.EXISTED_FAIL_HINT)

            loan_data = self.query(parsed,log_db)
            transed = self.trans(loan_data,log_db)
            self.save_cache(parsed,transed,log_db)
            self.save_log(self.RIGHT,log_db)
            return transed.val,True
        except:
            self.save_log(self.WRONG, log_db)
            logger.error("shareLoanInfo91 failed",exc_info=True)
            return "",False

    def verify(self,rcv:str,log_db):
        try:
            assert len(rcv) > 0
            log_db.verify_rcv = self.RIGHT
            logger.info("verify receive success")
        except:
            logger.error(self.Error.ILLEAGL_NOTE,exc_info = True)
            log_db.verify_rcv = self.WRONG
            log_db.note = self.Error.ILLEAGL_NOTE
            raise Exception("verify receive => False")

    def parse(self,rcv:bytes,log_db)->dict:
        try:
            to_list = rcv.decode().split("|")
            assert len(to_list) == self.ZX_LENGTH
            assert to_list[3] == self.Code.SHARE_REQ_CODE
            user_data = self.zhengxin_decode(to_list[6])
            log_db.parse_res = self.RIGHT
            logger.info("parse success")
            return user_data
        except:
            logger.error("parse failed",exc_info = True)
            log_db.parse_res = self.WRONG
            raise Exception("parse failed")

    def verify_meanful_rcv(self,parsed,log_db):
        name, idcard, _ = self._user_info(parsed)
        log_db.name = name
        log_db.idcard = idcard
        if self.notEmptyDict(parsed) == False:
            log_db.not_empty = self.WRONG
            raise Exception("notEmptyDict => False")
        log_db.not_empty = self.RIGHT

    def verify_query(self,parsed,log_db):
        loan_info, status_q = self.query(parsed)
        if status_q == False:
            log_db.query_table = self.WRONG
            raise Exception("status_q => False")
        log_db.query_table = self.RIGHT
        return loan_info

    def query(self,parsed:dict,log_db)->dict:
        try:
            zx = self.ZhengXin91LoanCoreInfo
            loan_info = self.make_module(parsed)
            loan_infos = {"loan_infos":[loan_info]}
            state = loan_info[zx.BORROWSTATE]
            if state == self._borrowState().loaned:
                uid,_ = self._has_applied(parsed)
                JkUserLoanRecord,_ = self._has_loaned(uid)
                loan_info[zx.BORROWAMOUNT] = JkUserLoanRecord.amount
                loan_info[zx.CONTRACTDATE] = JkUserLoanRecord.pay_time
            log_db.query_table = self.RIGHT
            logger.info("query success")
            return loan_infos
        except:
            log_db.query_table = self.WRONG
            logger.error("query failed",exc_info=True)
            raise Exception("query")

    def trans(self,loan_data:dict,log_db)->namedtuple:
        S = self.step_return()
        try:
            encoded = self.zhengxin_encode(loan_data)
            log_db.trans_res = self.RIGHT
            logger.info("trans success")
            return S(val=self.make_resp_template(encoded),res=False)
        except:
            log_db.trans_res = self.WRONG
            logger.error("trans failed",exc_info=True)
            raise Exception("trans failed")

    def save_cache(self,parsed:dict,transed:namedtuple,log_db):
        try:
            name, idcard, _ = self._user_info(parsed)
            zx = ZhengXin91ShareOriData()
            zx.name = name
            zx.idcard = idcard
            zx.status_code = self.Code.SHARE_EXISTED
            zx.ori_data = transed.val
            zx.ctime_stamp = self.now_stamp
            zx.save()
            log_db.save_cache = self.RIGHT
            logger.info("save cache success")
        except:
            log_db.save_cache = self.WRONG
            logger.error("save_cache",exc_info=True)
            raise Exception("save cache failed")

    def extract_not_expire(self,parsed)->namedtuple:
        ori_data = self.got_not_expired(parsed)
        return ori_data

    def got_not_expired(self,parsed)->str:
        name, idcard, companyCode = self._user_info(parsed)
        ori = ZhengXin91ShareOriData
        ori_data = ori.objects.filter(idcard=idcard).order_by("id")[:1][0].ori_data
        return ori_data

    def make_module(self,parsed)->dict:
        zx = self.ZhengXin91LoanCoreInfo
        loan_info = {
            zx.BORROWTYPE: 1,
            zx.BORROWSTATE: self.which_borrow_state(parsed),
            zx.BORROWAMOUNT: 0,
            zx.CONTRACTDATE: "0",
            zx.LOANPERIOD: 0,
            zx.REPAYSTATE: 0,
            zx.ARREARSAMOUNT: 0,
            zx.COMPANYCODE: self.Authentication.COMPANY_CODE,
        }
        return loan_info

    def which_borrow_state(self,parsed:dict)->int:
        uid,apply = self._has_applied(parsed)
        if apply:
            _,loan = self._has_loaned(uid)
            if loan:
                return self._borrowState().loaned
            else:
                return self._borrowState().refused
        else:
            return self._borrowState().unknow

    def _has_loaned(self,uid:str)->(JkUserLoanRecord,bool):
        res = JkUserLoanRecord.objects.using(self.JKWEB).filter(uid=uid)
        if len(res) == 0:
            return "",False
        else:
            return res[0],True

    def _has_applied(self,parsed:dict)->(str,bool):
        name, idcard, _ = self._user_info(parsed)
        queryRes = JkLoanApply.objects.using(self.JKWEB).filter(name=name)
        if len(queryRes) == 0:
            return "",False
        else:
            uid = queryRes.order_by("-id")[:1][0].uid
            return uid,True

    def _borrowState(self):
        BS = namedtuple("borrowState","unknow refused loaned")
        states = BS(unknow=0,refused=1,loaned=2)
        return states

    def _user_info(self, py_obj) -> tuple:
        name = py_obj[self.UserInfo.REC_NAME]
        idcard = py_obj[self.UserInfo.REC_IDCARD]
        companyCode = py_obj[self.UserInfo.COMPANYCODE]
        return name,idcard,companyCode

    def make_resp_template(self,encoded:str)->str:
        code = self.Authentication.COMPANY_CODE
        share_num = self.Code.SHARE_RESP_NUM
        resp_template = f"01|{code}|01|{share_num}|01|01|{encoded}|0000||"
        return resp_template


