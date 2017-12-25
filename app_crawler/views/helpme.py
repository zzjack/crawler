import json
from django.http import JsonResponse
from django.views.generic.base import View
from app_crawler.storage.huadao import infos as HD
from crawler.settings import logger
from app_crawler.views.manager import Manager

class DataStruct:
    idcard = ""
    name = ""
    phone = ""
    token = ""
    flag = ""
    seqId = ""
    err = dict()

class viewManager(Manager):
    def parse_ReceivedData(self,request)->DataStruct:
        d = DataStruct()
        try:
            parse_res = json.loads(request.body)
            d.idcard = parse_res.get(self.post_idcard,"empty")
            d.name = parse_res.get(self.post_name,"empty")
            d.phone = parse_res.get(self.post_phone,"empty")
            d.token = parse_res.get(self.post_token,"empty")
            d.seqId = parse_res.get(self.post_seqId,"empty")
            d.flag = parse_res.get(self.flag,"empty")
        except:
            print("accept request.body ==>",request.body)
            logger.error("",exc_info=True)
        return d

#贷啦/海米/helpme
class helpMe(View,viewManager):

    def get(self,request)->JsonResponse:
        logger.info(f"this is {request.method}")
        return JsonResponse(self.illegal_request_resp)

    def post(self,request)->JsonResponse:
        logger.info("helpme accept post info")
        post_info = self.parse_ReceivedData(request)
        # handle post data is empty
        if len(post_info.err) > 0:
            logger.info(post_info.err)
            return JsonResponse(post_info.err)
        # instantiation hd_interface/Hd_EMW025....
        logger.info("helpme instantiation hd_interface and hd saving")
        hdsave = HD.hd_interface()
        # multiple equals is used to storage
        hdsave.name =  post_info.name
        hdsave.idcard = post_info.idcard
        hdsave.token = post_info.token
        hdsave.phone = post_info.phone
        hdsave.flag =  post_info.flag
        hdsave.seqId = post_info.seqId
        logger.info(f"helpme accepted arguments:{hdsave.name},{hdsave.idcard},{hdsave.token},{hdsave.phone},{hdsave.flag}")
        # 2017/10/24/10:20 => add storage in helpMe's database
        res = hdsave.main()
        # store emd008 details in database boshidun.
        hdsave.emd008_details_storage(flag="HM")
        logger.info(res.get("retmessage"))
        return JsonResponse(res)

