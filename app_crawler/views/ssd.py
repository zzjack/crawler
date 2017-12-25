import logging
from django.http import JsonResponse
from django.views.generic.base import View
from app_crawler.storage.huadao import infos as HD
from app_crawler.views.helpme import viewManager
from app_crawler.storage.huadao.manager import storageMsg

logger = logging.getLogger(__name__)

# EMW025 黑名单模糊汇总查询
class SSDEMW025(View,viewManager):
    def get(self,request)->JsonResponse:
        return JsonResponse(self.illegal_request_resp)
    def post(self,request)->JsonResponse:
        post_info = self.parse_ReceivedData(request)
        hd = HD.hd_interface()
        hd.flag = post_info.flag
        hd.phone = post_info.phone
        hd.name = post_info.name
        hd.idcard = post_info.idcard
        hd.seqId = post_info.seqId
        res = hd.hd_blackList()
        logger.info("Accepted_Query EMW025 黑名单模糊汇总查询")
        return JsonResponse(res)

# EMR004 贷款申请次数(被整合到08接口去了)
class SSDEMR003(View,viewManager,storageMsg):
    def get(self,request)->JsonResponse:
        return JsonResponse(self.illegal_request_resp)
    def post(self,request)->JsonResponse:
        post_info = self.parse_ReceivedData(request)
        hd = HD.hd_interface()
        hd.flag = post_info.flag
        hd.phone = post_info.phone
        hd.name = post_info.name
        hd.idcard = post_info.idcard
        hd.seqId = post_info.seqId
        res1 = hd.ssd_webloan()
        # storage cfd_hy_webloan_detail;cfd_hd_creditregistration
        res2 = hd.hd_webloan()
        res3 = hd.hd_webloandetail()
        if res1.get(self.retcode_name) == res2.get(self.retcode_name) \
                == res3.get(self.retcode_name) == self.retcode_success:
            return_res = self.SUCCESS
        else:
            return_res = self.FAILED
        logger.info("Accepted_Query EMR004 贷款申请次数")
        return JsonResponse(return_res)

# EMW005运营商实名认证
class SSDPhoneRZlist(View,viewManager):
    def get(self,request)->JsonResponse:
        return JsonResponse(self.illegal_request_resp)
    def post(self,request)->JsonResponse:
        post_info = self.parse_ReceivedData(request)
        hd = HD.hd_interface()
        hd.phone = post_info.phone
        hd.flag = post_info.flag
        hd.name = post_info.name
        hd.idcard = post_info.idcard
        hd.seqId = post_info.seqId
        res = hd.hd_operator_rz()
        logger.info("Accepted_Query EMW005运营商实名认证")
        return JsonResponse(res)

# EMW018 不良信息查询
class SSDIllegalInfo(View,viewManager):
    def get(self,request)->JsonResponse:
        return JsonResponse(self.illegal_request_resp)
    def post(self,request)->JsonResponse:
        post_info = self.parse_ReceivedData(request)
        hd = HD.hd_interface()
        hd.phone = post_info.phone
        hd.flag = post_info.flag
        hd.name = post_info.name
        hd.idcard = post_info.idcard
        hd.seqId = post_info.seqId
        res = hd.hd_illegal_info()
        logger.info("Accepted_Query EMW018 illegalinfo")
        return JsonResponse(res)

