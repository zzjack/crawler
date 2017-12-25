import json
from django.http import JsonResponse,HttpResponse
from django.views.generic.base import View
from app_crawler.views import helpme as basic
from app_crawler.storage.zhengxin91.infos import ZhengXin91
from app_crawler.storage.zhengxin91.shared_infos import  ZhengXin91Shared
from app_crawler.storage.zhengxin91.shared_infos_failed import UnexpectedHandler
from crawler.settings import logger


class ZhengXin91Storage(View,basic.viewManager):
    def get(self,request)->JsonResponse:
        example = {"flag":"HM",'realName': '陈水金', 'idCard': '350424198301082038'}
        return JsonResponse(example)

    def post(self,request)->JsonResponse:
        try:
            py_obj = json.loads(request.body)
            zx = ZhengXin91()
            if zx.main(py_obj):
                logger.info("Accepted_Query: zhengxin91storage")
                return JsonResponse(self.success)
            else:
                raise Exception("zhengxin91 query or storatrge error")
        except:
            logger.error("zhengxin91 error traceback",exc_info=True)
            return JsonResponse(self.classNum_empty)


class ZhengXin91Share(View,basic.viewManager):
    def post(self,request)->HttpResponse:
        default_data = ""
        try:
            zx = ZhengXin91Shared()
            resp,state = zx.main(request.body)
            if state:
                logger.info("query table success")
                return HttpResponse(resp)
            else:
                logger.info("query failed,using default data")
                e = UnexpectedHandler()
                default_data = e.except_resp(request.body)
                return HttpResponse(default_data)
        except:
            logger.error("Exception error",exc_info = True)
            return HttpResponse(default_data)





