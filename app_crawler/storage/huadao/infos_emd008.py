from crawler.settings import logger
from app_crawler.models import HDEMD008EMR004,HDEMD008EMR007,HDEMD008EMR009
from app_crawler.models import HDEMD008EMR012,HDEMD008EMR013
from app_crawler.models import HDEMD008Manager,HDEMD008EMR002


class EMD008:
    code = "0"
    phone = "0"
    province = "0"
    city = "0"
    result = []

    def __init__(self,name:str,idcard:str,phone:str,data:dict,db_name:str):
        self.name = name
        self.idcard = idcard
        self.phone = phone
        self.data = data
        self.flag = db_name

    def main(self):
        if len(self.data) != 5:
            logger.info("hd emd008 response is {},empty!")
            self.store_emd008()
            return
        self.parse_data()
        emd_id = self.store_emd008()
        if len(self.result) == 0:
            logger.info("hd emd008 loan details are empty")
        else:
            self.store_detail(emd_id)

    def store_detail(self,emd_id:int):
        msg = "hd emd008 loan detail"
        try:
            for r in self.result:
                if len(r) == 0:
                    logger.info("one of hd emd008 details is empty")
                else:
                    setattr(EMD008Detail,"emd_id",emd_id)
                    setattr(EMD008Detail,"name",self.name)
                    setattr(EMD008Detail,"idcard",self.idcard)
                    setattr(EMD008Detail,"phone",self.phone)
                    setattr(EMD008Detail,"flag",self.flag)
                    setattr(EMD008Detail,"cycle",r["CYCLE"])
                    emd008 = EMD008Detail()
                    func = getattr(emd008,r["TYPE"])
                    func(r["DATA"])
            logger.info(f"{msg} successfully stored")
        except:
            logger.error(f"{msg} failed",exc_info=True)

    def parse_data(self):
        try:
            self.code = self.data["CODE"]
            self.province = self.data["PROVINCE"]
            self.city = self.data["CITY"]
            self.result = self.data["RESULTS"]
            logger.info(f"emd008 parse succeed,{self.code},{self.phone},{self.province},{self.city}")
        except:
            err = "emd008 parse failed"
            logger.error(err,exc_info = True)
            raise Exception(err)

    def store_emd008(self)->int:
        hd = HDEMD008Manager()
        hd.name = self.name
        hd.phone =  self.phone
        hd.idcard = self.idcard
        hd.code = self.code
        hd.province = self.province
        hd.city = self.city
        hd.result = "0" if len(self.result) == 0 else "1"
        hd.save(using=self.flag)
        saved_id = hd.id
        logger.info(f"store in HDEMD008Manager id is {saved_id}")
        return saved_id

class EMD008Detail:
    emd_id = ""
    name = ""
    idcard = ""
    phone = ""
    flag = ""
    cycle = ""
    def EMR002(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR002(
                    emd_id = self.emd_id,
                    name=self.name,
                    mobile=self.phone,
                    idcard=self.idcard,
                    cycle=self.cycle,
                    platform_code=d.get("PLATFORMCODE", "empty"),
                    register_time=d.get("REGISTERTIME", "empty"),
                    p_type = d.get("P_TYPE", "empty"),
                )
            )
        HDEMD008EMR002.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr002 save succeed")
    def EMR004(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR004(
                    emd_id=self.emd_id,
                    name = self.name,
                    mobile = self.phone,
                    idcard = self.idcard,
                    cycle = self.cycle,
                    platform_code = d.get("PLATFORMCODE", "empty"),
                    application_time = d.get("APPLICATIONTIME", "empty"),
                    application_amount = d.get("APPLICATIONAMOUNT", "empty"),
                    application_result = d.get("APPLICATIONRESULT", "empty"),
                    p_type = d.get("P_TYPE", "empty"),
                )
            )
        HDEMD008EMR004.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr004 save succeed")
    def EMR007(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR007(
                    emd_id=self.emd_id,
                    name = self.name,
                    mobile = self.phone,
                    idcard = self.idcard,
                    cycle = self.cycle,
                    platform_code = d.get("PLATFORMCODE", "empty"),
                    loan_lenders_time = d.get("LOANLENDERSTIME", "empty"),
                    loan_lenders_amount = d.get("LOANLENDERSAMOUNT", "empty"),
                    p_type = d.get("P_TYPE", "empty"),
                )
            )
        HDEMD008EMR007.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr007 save succeed")
    def EMR009(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR009(
                    emd_id=self.emd_id,
                    name = self.name,
                    mobile = self.phone,
                    idcard = self.idcard,
                    cycle = self.cycle,
                    rejection_time = d.get("REJECTIONTIME", "empty"),
                    platform_code = d.get("PLATFORMCODE", "empty"),
                    p_type = d.get("P_TYPE", "empty"),
                )
            )
        HDEMD008EMR009.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr009 save succeed")
    def EMR012(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR012(
                    emd_id=self.emd_id,
                    name = self.name,
                    mobile = self.phone,
                    idcard = self.idcard,
                    cycle = self.cycle,
                    platform = d.get("PLATFORM", "empty"),
                    counts = d.get("COUNTS", "empty"),
                    money = d.get("MONEY", "empty"),
                    d_time = d.get("D_TIME", "empty"),
                )
            )
        HDEMD008EMR012.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr012 save succeed")
    def EMR013(self,data:dict):
        emr = []
        for d in data:
            emr.append(
                HDEMD008EMR013(
                    emd_id=self.emd_id,
                    name = self.name,
                    mobile = self.phone,
                    idcard = self.idcard,
                    cycle = self.cycle,
                    platform = d.get("PLATFORM", "empty"),
                    money = d.get("MONEY", "empty"),
                )
            )
        HDEMD008EMR013.objects.using(self.flag).bulk_create(emr)
        logger.info("emd008:emr013 save succeed")