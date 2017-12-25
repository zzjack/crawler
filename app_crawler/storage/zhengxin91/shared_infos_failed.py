from app_crawler.models import ZhengXin91ShareLog
from app_crawler.storage.zhengxin91.shared_infos import ZhengXin91Shared


class UnexpectedHandler(ZhengXin91Shared):
    def except_resp(self,rcv:bytes)->str:
        log_db = ZhengXin91ShareLog()
        try:
            to_list = rcv.decode().split("|")
            assert len(to_list) == self.ZX_LENGTH
            assert to_list[3] == self.Code.SHARE_REQ_CODE
            parsed = self.zhengxin_decode(to_list[6])
            name, idcard, _ = self._user_info(parsed)
            log_db.name = name
            log_db.idcard = idcard
            loan_info = self.make_module(parsed)
            loan_data = {"loan_infos": [loan_info]}
            encoded = self.zhengxin_encode(loan_data)
            log_db.status =  self.RIGHT
            log_db.note = "no data or unexpected error"
            log_db.save()
            return self.make_resp_template(encoded)
        except:
            log_db.status = self.WRONG
            log_db.note = "UnexpectedHandler encountered error"
            log_db.save()