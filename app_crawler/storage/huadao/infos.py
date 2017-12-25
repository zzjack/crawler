import requests
import json
import pymysql
import datetime,time
import re
import traceback
from app_crawler.models import *
from crawler.settings import logger
from app_crawler.storage.huadao.manager import HDInterfaceUrl
from app_crawler.storage.huadao.manager import storageMsg
from app_crawler.storage.huadao.infos_emd008 import EMD008


Ctime = datetime.datetime.now()

# 2017/10/26 发现一个修改线程引起的错误。共享了内存。
# 2017/10/27 modify all ori_sql to orm

# 2017/11/05 add new function:for HM storage,judge expiration of data before crawling every time.
# only operator_RZ expiration = 360,others expiration = 7

class DB(object):
    def __init__(self,host,port,usr,pwd,dbName):
        self.host = host
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.dbName = dbName
    def exe_sql(self, sqlString, values):
        db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.usr,
            passwd=self.pwd,
            db=self.dbName,
            charset='utf8'
        )
        cursor = db.cursor()
        try:
            cursor.execute(sqlString, values)
            if sqlString.split()[0] == "select":
                returnData = cursor.fetchall()
                return returnData
            else:
                db.commit()
            return True
        except:
            logger.error("exe_sql error",exc_info = True)
            print("ERROR SQL & VAL",sqlString, values)
            db.rollback()
            traceback.print_exc()
            return False
        finally:
            cursor.close()

class hd_interface(storageMsg,HDInterfaceUrl):
    queryId = Ctime
    reXml = re.compile("<string.*>(.*)</string>")
    ctime = Ctime
    BSDFLAG = "HM"
    SSDFLAG = "SSD"
    SSDWEBLOANCYCLE = "3" #根据库中已有的记录，设定为3的。
    HMDB = "helpMe"
    SSDDB = "ssd"
    def __int__(self,name:str,idcard:str,token:str,phone:str,hdAccountInfo:dict,seqId:str,flag:str):
        self.hdAccountInfo = hdAccountInfo
        self.name = name
        self.idcard = idcard
        self.token = token
        self.phone = phone
        self.seqId = seqId
        self.flag = flag
    def req_hdInterface(self,url,data:dict)->dict:
        if data == "":
            complete_url = url
        else:
            url_data = "{url}?&".format(url=url)
            for k,v in data.items():
                d = "{k}={v}&".format(k=k,v=v)
                url_data += d
            complete_url = url_data
        getRes = requests.get(complete_url,"")
        reRes = self.reXml.findall(getRes.text)
        if len(reRes) == 1:
            try:
                res = json.loads(reRes[0])
            except:
                res={}
            return res
        else:
            return {}
    def _get_newtoken(self,table)->str:
        token = ""
        try:
            if table ==  hd_token.__name__:
                t = hd_token.objects.using("ssd").values("token").order_by("-id")
                assert len(t) > 0
                token = t[0].get("token","")
            elif table == hd_tokenwebloan.__name__:
                t = hd_tokenwebloan.objects.using("ssd").values("token").order_by("-id")
                assert len(t) > 0
                token = t[0].get("token","")
            else:
                Exception("_get_newtoken unexpect!")
                logger.error("ERROR",exc_info=True)
        except:
            logger.error("get newtoken error",exc_info=True)
            raise Exception("get newtoken error")
        logger.info(f"get newtoken {token} from {table}")
        return token
    def emd008_details_storage(self,flag):
        # crawler
        token = self._get_newtoken("hd_tokenwebloan")
        data = dict(
            Phone=self.phone,
            # because the document "haimifengkongmoxing" do not figure out the cycle,default the cycle = 24.
            cycle=24,
            Platform=0,
            ACCESS_TOKEN=token,
        )
        parseRes = self.req_hdInterface(self.hdEMD008Url, data)
        data = json.dumps(parseRes)
        # storage
        db_name = ""
        if flag == self.BSDFLAG:
            db_name = self.HMDB
        elif flag == self.SSDFLAG:
            db_name = self.SSDDB
        else:
            logger.error(f"Unexpect flag {flag};function _EMD008_details_storage")
        e = EMD008(data=data, idcard=self.idcard, phone=self.phone, name=self.name, db_name=db_name)
        e.main()
    def _EMD008_integrate_interface(self,cycle)->dict:
        #crawler
        token = self._get_newtoken("hd_tokenwebloan")
        data = dict(
            Phone = self.phone,
            cycle = cycle,
            Platform = 0,
            ACCESS_TOKEN = token,
        )
        parseRes = self.req_hdInterface(self.hdEMD008Url,data)
        # storage
        ori = Hd_EMD008()
        ori.flag = self.flag
        ori.idcard = self.idcard
        ori.phone = self.phone
        ori.name = self.name
        ori.ori_data = json.dumps(parseRes)
        ori.save()
        return parseRes

    def datetime_timestamp(self,dt):
        if dt == "":
            dt = "2010-11-02 15:20:04"
        time.strptime(dt.__str__(),'%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt.__str__(), '%Y-%m-%d %H:%M:%S'))
        return int(s)

    def dayTosecond(self,day:int)->int:
        return day * 24 * 60 * 60

    def x_days_ago(self,x:int)->int:
        now = int(time.time())
        x_day = self.dayTosecond(x)
        return now - x_day

    def detect_expire(self,dt:str,limit=7)->bool:
        detected_time = self.datetime_timestamp(dt)
        x_day_ago = self.x_days_ago(limit)
        if detected_time - x_day_ago <= 0:
            return True
        else:
            return False
    def _hd_blackList_judge_before_crawl(self,data:dict)->dict:
        try:
            bsd_n = bsd_hy_blacklist_hit_summary
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_person_id=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                parseRes = self.req_hdInterface(self.hdBlackListUrl, data)
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime):
                    parseRes = self.req_hdInterface(self.hdBlackListUrl, data)
                else:
                    parseRes = {
                        "WDHMDCOUNT": cln.black_hit_count,
                    }
        except:
            logger.error("_hd_blackList_judge_before_crawl",exc_info = True)
            parseRes = self.req_hdInterface(self.hdBlackListUrl, data)
        return  parseRes
    def hd_blackList(self)->dict:
        # EMW025 黑名单模糊汇总查询
        try:
            # crawler
            token = self._get_newtoken("hd_token")
            data = dict(
                idcard=self.idcard,
                ACCESS_TOKEN=token,
            )
            # storage
            if self.flag == self.BSDFLAG:
                ## storage in bsd_hy_blacklist_hit_summary
                parseRes = self._hd_blackList_judge_before_crawl(data)
                bsd = bsd_hy_blacklist_hit_summary()
                bsd.p_person_id = self.idcard
                bsd.p_person_name = self.name
                bsd.p_phone = self.phone
                bsd.query_id = self.queryId
                bsd.status =  "1000"
                bsd.black_risk_type = "网贷黑名单"
                bsd.black_hit_count = parseRes.get("WDHMDCOUNT","")
                bsd.save(using=self.HMDB)
                # storage in bsd_blacklisthitnum
                db = bsd_blacklisthitnum()
                db.seq_id = self.seqId
                db.p_person_id = self.idcard
                db.black_risk_type = ""
                db.black_hit_count = parseRes.get("WDHMDCOUNT",0)
                db.CODE = "200"
                db.data_source = "hd"
                db.save(using=self.HMDB)
            elif self.flag == self.SSDFLAG:
                parseRes = self.req_hdInterface(self.hdBlackListUrl, data)
                ssd = cfd_hd_huifamohufact()
                ssd.p_idcode = self.idcard
                ssd.status = parseRes.get("CODE","")
                ssd.totalnumber = parseRes.get("totalCount","")
                ssd.casenumber = parseRes.get("ajlcCount","")
                ssd.zhixinnumber = parseRes.get("zxggCount","")
                ssd.taxnumber = ""
                ssd.cuiqiannumber = ""
                ssd.kaitinnumber = parseRes.get("ktggCount","")
                ssd.othernumber = ""
                ssd.shenpannumber = parseRes.get("cpwsCount","")
                ssd.wangdainumber = parseRes.get("wdhmdCount","")
                ssd.success = "200"
                ssd.save(using=self.SSDDB)
                # storage in crawler
                ori = Hd_EMW025()
                ori.flag = self.flag
                ori.idcard = self.idcard
                ori.phone = self.phone
                ori.name = self.name
                ori.ori_data = json.dumps(parseRes)
                ori.save()
        except:
            logger.error("hd_blackList failed",exc_info=True)
            return self.FAILED
        logger.info("EMW025 黑名单模糊汇总查询 success")
        return self.SUCCESS

    def _hd_blackList_detail_judge_before_crawl(self)->dict:
        try:
            bsd_n = bsd_hy_blacklist_hit_detail
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_person_id=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                res = self._EMD008_integrate_interface("24")
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime):
                    res = self._EMD008_integrate_interface("24")
                else:
                    res = {
                        "RESULTS": [
                            {}, {}, {}, {},
                            {"DATA": [
                                {
                                    "MONEY": cln.overdue_amount_most,
                                    "COUNTS": cln.overdue_count,
                                    "D_TIME": cln.overdue_time_latest,
                                }
                            ]}
                        ]
                    }
        except:
            logger.error("_hd_blackList_detail_judge_before_crawl",exc_info=True)
            res = self._EMD008_integrate_interface("24")
        return res
    def hd_blackList_detail(self)->dict:
        # EMR012 逾期平台详情查询
        try:
            res = self._hd_blackList_detail_judge_before_crawl()
            default = [{},{},{},{},{}]
            EMR012 = res.get("RESULTS",default)[4].get("DATA",{})
            bsd = bsd_hy_blacklist_hit_detail()
            if len(EMR012) == 0:
                bsd.p_person_id = self.idcard
                bsd.query_id = self.queryId
                bsd.status = "1000"
                bsd.black_risk_type = ""
                bsd.overdue_amount_most = ""
                bsd.overdue_count = ""
                bsd.overdue_days_most = ""
                bsd.overdue_time_latest = self.ctime
                bsd.save(using=self.HMDB)
            else:
                for i in EMR012:
                    black_risk_type = "网络平台逾期信息" #黑名单风险类型
                    overdue_amount_most = i.get("MONEY","") #最高逾期金额
                    overdue_count = i.get("COUNTS","") #贷款逾期笔数
                    overdue_time_latest = i.get("D_TIME","") #最近逾期时间
                    bsd.p_person_id = self.idcard
                    bsd.query_id = self.queryId
                    bsd.status = "1000"
                    bsd.black_risk_type = black_risk_type
                    bsd.overdue_amount_most = overdue_amount_most
                    bsd.overdue_count = overdue_count
                    bsd.overdue_days_most = ""
                    bsd.overdue_time_latest = overdue_time_latest
                    bsd.save(using=self.HMDB)
        except:
            logger.error("hd_blackList_detail EMR012 =>",exc_info=True)
            return self.FAILED
        logger.info("EMR012 逾期平台详情查询 success")
        return self.SUCCESS
    def _hd_illegal_info_judge_before_crawl(self,data:dict)->dict:
        try:
            bsd_n = bsd_hy_illegalinfo_summary
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_person_id=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                parseRes = self.req_hdInterface(self.hdIllegalInfoUrl, data)
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime):
                    parseRes = self.req_hdInterface(self.hdIllegalInfoUrl, data)
                else:
                    parseRes = {
                        "RESULTDESC": cln.result,
                        "MESSAGE": cln.resultdesc,
                    }
        except:
            logger.error("_hd_illegal_info_judge_before_crawl",exc_info = True)
            parseRes = self.req_hdInterface(self.hdIllegalInfoUrl, data)
        return parseRes
    def hd_illegal_info(self)->dict:
        # EMW018不良信息查询,
        # http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx?op=Get_EMW_IllegalInfo_BLXXCX
        try:
            # crawler
            token = self._get_newtoken("hd_token")
            data = dict(
                name=self.name,
                idcard=self.idcard,
                ACCESS_TOKEN=token,
            )
            if self.flag == self.BSDFLAG:
                parseRes = self._hd_illegal_info_judge_before_crawl(data)
                bsd = bsd_hy_illegalinfo_summary()
                bsd.seq_id = self.seqId
                bsd.p_person_id = self.idcard
                bsd.p_person_name = self.name
                bsd.CODE = "200"
                bsd.result = parseRes.get("RESULTDESC","")
                bsd.resultdesc = parseRes.get("MESSAGE","")
                bsd.save(using=self.HMDB)
            elif self.flag == self.SSDFLAG:
                parseRes = self.req_hdInterface(self.hdIllegalInfoUrl, data)
                ssd = cfd_hd_IllegalInfo_BLXXCX()
                ssd.p_person_id = self.idcard
                ssd.p_person_name = self.name
                ssd.CODE = "200"
                ssd.result = parseRes.get("RESULTDESC","")
                ssd.resultdesc = parseRes.get("MESSAGE","")
                ssd.save(using=self.SSDDB)
                # storage Hd_EMW018
                ori = Hd_EMW018()
                ori.flag = self.flag
                ori.idcard = self.idcard
                ori.phone = self.phone
                ori.name = self.name
                ori.ori_data = json.dumps(parseRes)
                ori.save()
        except:
            logger.error("EMW018不良信息查询 =>",exc_info=True)
            return self.FAILED
        logger.info(f"{self.flag} {self.name},{self.idcard} insert into success")
        return self.SUCCESS
    def _hd_operator_rz_judge_before_crawler(self,data:dict)->dict:
        try:
            bsd_n = bsd_hy_operator_rz
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_person_id=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                parseRes = self.req_hdInterface(self.hdOperatorRzUrl, data)
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime,limit=360):
                    parseRes = self.req_hdInterface(self.hdOperatorRzUrl, data)
                else:
                    parseRes = {
                        "CODE": cln.CODE,
                        "CID": cln.person_id,
                        "NAME": cln.person_name,
                        "PHONE": cln.phone,
                        "RESULT": cln.result,
                        "RESULTDESC": cln.resultdesc,
                    }
        except:
            logger.error("_hd_operator_rz_judge_before_crawler",exc_info = True)
            parseRes = self.req_hdInterface(self.hdOperatorRzUrl, data)
        return parseRes
    def hd_operator_rz(self)->dict:
        # EMW005运营商实名认证
        # http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx?op=Get_EMW_Operator_RZ
        # crawler
        parseRes = {}
        try:
            token = self._get_newtoken("hd_token")
            data = dict(
                name=self.name,
                idcard=self.idcard,
                phone=self.phone,
                ACCESS_TOKEN=token
            )
            if self.flag == self.BSDFLAG:
                parseRes = self._hd_operator_rz_judge_before_crawler(data)
                hd = bsd_hy_operator_rz()
                hd.p_person_id = self.idcard
                hd.p_person_name = self.name
                hd.p_phone = self.phone
                hd.query_id = self.queryId
                hd.CODE = parseRes.get("CODE","")
                hd.person_id = parseRes.get("CID","")
                hd.person_name = parseRes.get("NAME","")
                hd.phone = parseRes.get("PHONE","")
                hd.result = parseRes.get("RESULT","")
                hd.resultdesc = parseRes.get("RESULTDESC","")
                hd.channel_name = "HD"
                hd.save(using=self.HMDB)
            elif self.flag == self.SSDFLAG:
                parseRes = self.req_hdInterface(self.hdOperatorRzUrl, data)
                # storage in hd_emw005
                ori = Hd_EMW005()
                ori.flag = self.flag
                ori.idcard = self.idcard
                ori.phone = self.phone
                ori.name = self.name
                ori.ori_data = json.dumps(parseRes)
                ori.save()
                # storage in cfd_hd_operator_rz
                ssd = cfd_hd_operator_rz()
                ssd.p_person_id = self.idcard
                ssd.p_person_name = self.name
                ssd.p_phone = self.phone
                ssd.query_id = self.queryId
                ssd.CODE = parseRes.get("CODE","")
                ssd.person_id = parseRes.get("CID","")
                ssd.person_name = parseRes.get("NAME","")
                ssd.phone = parseRes.get("PHONE","")
                ssd.result = parseRes.get("RESULT","")
                ssd.resultdesc = parseRes.get("RESULTDESC","")
                ssd.channel_name = "HD"
                ssd.save(using=self.SSDDB)
        except:
            logger.error("error =>",exc_info=True)
            new_failed = {"retcode":-1, "retmessage": "failed", "operator_res":""}
            return new_failed
        logger.info("EMW005运营商实名认证")
        new_success = {
            "retcode": 0,
            "retmessage": "succeed",
            "operator_res":parseRes.get("RESULT","-1"),
            "operator_desc":parseRes.get("RESULTDESC",""),
        }
        return new_success
    # 3,6,9,12,24
    def hd_webloan(self)->dict:
        # EMR002 信贷平台注册详情，统计这个接口的数量
        try:
            for cycle in ("3","6","9","12","24"):
                self._hd_webloan(cycle)
        except:
            logger.error("EMR002 =>", exc_info=True)
            return self.FAILED
        logger.info("EMR002 信贷平台注册详情/webloan success")
        return self.SUCCESS
    def _hd_webloan_judge_before_crawl(self,cycle:str)->int:
        try:
            bsd_n = bsd_hy_webloan
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_id_card=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                logger.info("crawl from third interface...")
                res = self._EMD008_integrate_interface(cycle)
                register_num = len(res.get("RESULTS",[{}])[0].get("DATA",{}))
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime):
                    logger.info("crawl from third interface...")
                    res = self._EMD008_integrate_interface(cycle)
                    register_num = len(res.get("RESULTS", [{}])[0].get("DATA", {}))
                else:
                    logger.info("related data have existed")
                    register_num = cln.ttl_hit_count
        except:
            logger.error("_hd_webloan_judge_before_crawl",exc_info = True)
            res = self._EMD008_integrate_interface(cycle)
            register_num = len(res.get("RESULTS", [{}])[0].get("DATA", {}))
        return register_num
    def _hd_webloan(self,cycle:str)->None:
        #storage
        if self.flag == self.BSDFLAG:
            register_num = self._hd_webloan_judge_before_crawl(cycle)
            bsd = bsd_hy_webloan()
            bsd.p_name = self.name
            bsd.p_phone = self.phone
            bsd.p_id_card = self.idcard
            bsd.result_code = "200"
            bsd.product_res_code = "1000"
            bsd.query_id = self.queryId
            bsd.query_time = str(int(time.time())) + "000"
            bsd.ttl_hit_count = register_num
            bsd.ttl_hit_pname = "未发现"
            bsd.risk_level = ""
            bsd.save(using=self.HMDB)
        elif self.flag == self.SSDFLAG:
            res = self._EMD008_integrate_interface(cycle)
            EMR002 = res.get("RESULTS", [{}])[0]
            EMR002_cycle = EMR002.get("CYCLE", "")
            EMR002_data = EMR002.get("DATA", {})
            register_num = len(EMR002_data)
            ssd = cfd_hd_creditregistration()
            ssd.p_phone = self.phone
            ssd.p_cycle = cycle
            ssd.p_Platform = "0"
            ssd.CODE = "200"
            ssd.CYCLE = EMR002_cycle
            ssd.REGISTERNUM = register_num
            ssd.save(using=self.SSDDB)

    def _save_bsd_loanapplicationnum(self,cycle,times):
        try:
            logger.info(f"bsd_loanapplicationnum saved;user phone number=>{self.phone}")
            db = bsd_loanapplicationnum()
            db.seq_id = self.seqId
            db.p_Phone = self.phone
            db.p_cycle = cycle
            db.p_Platform = "0"
            db.CODE = "200"
            db.CYCLE = "".join((str(int(time.time())), "000"))
            db.LOANNUM = times
            db.data_source = "hd"
            db.save(using=self.HMDB)
        except:
            logger.error("error",exc_info=True)
    def _hd_webloandetail_oneCycle_judge_before_crawler(self,cycle:str)->int:
        try:
            bsd_n = bsd_hy_webloan
            queryRes = bsd_n.objects.using(self.HMDB).filter(p_id_card=self.idcard).order_by("-request_id")
            if len(queryRes) == 0:
                res = self._EMD008_integrate_interface(cycle)
                time = len(res.get("RESULTS",[{}])[0].get("DATA",{}))
            else:
                cln = queryRes[:1][0]
                if self.detect_expire(cln.ctime):
                    res = self._EMD008_integrate_interface(cycle)
                    time = len(res.get("RESULTS", [{}])[0].get("DATA", {}))
                else:
                    time = cln.ttl_hit_count
        except:
            logger.error("_hd_webloandetail_oneCycle_judge_before_crawler",exc_info = True)
            res = self._EMD008_integrate_interface(cycle)
            time = len(res.get("RESULTS", [{}])[0].get("DATA", {}))
        return time
    def _hd_webloandetail_oneCycle(self,cycle)->None:
        # EMR002 信贷平台注册详情，统计这个接口的数量
        if self.flag == self.BSDFLAG:
            logger.info(f"{self.BSDFLAG} _hd_webloandetail started")
            times = self._hd_webloandetail_oneCycle_judge_before_crawler(cycle)
            if times > 0:
                bsd = bsd_hy_webloan_detail()
                bsd.query_id = self.queryId
                bsd.period_name = f"webloan_hit_detail_m{cycle}"
                bsd.period_months = cycle
                bsd.class_name = "P2P网贷"
                bsd.class_count = times
                bsd.save(using=self.HMDB)
            self._save_bsd_loanapplicationnum(cycle,str(times))
            logger.info(f"{self.BSDFLAG} _hd_webloandetail ended")
        elif self.flag == self.SSDFLAG:
            logger.info(f"{self.SSDFLAG} _hd_webloandetail started")
            res = self._EMD008_integrate_interface(cycle)
            EMR002 = res.get("RESULTS",[{}])[0]
            EMR002_data = EMR002.get("DATA","")
            EMR002_cycle = EMR002.get("CYCLE","")
            times = len(EMR002_data)
            ssd = cfd_hy_webloan_detail()
            ssd.query_id = self.idcard
            ssd.period_name = EMR002_cycle
            ssd.period_months = int(cycle)
            ssd.class_name = "all"
            ssd.class_count = times
            ssd.save(using=self.SSDDB)
            logger.info(f"{self.SSDDB} _hd_webloandetail ended")
    def hd_webloandetail(self)->dict:
        try:
            logger.info("hd_webloandetail started")
            cycle = ["3","6","9","12","24"]
            for c in cycle:
                self._hd_webloandetail_oneCycle(c)
            logger.info("hd_webloandetail end")
        except:
            logger.error("hd_webloandetail=>",exc_info=True)
            return self.FAILED
        logger.info("webloandetail success")
        return self.SUCCESS
    def ssd_webloan(self):
        res = self._EMD008_integrate_interface(self.SSDWEBLOANCYCLE)
        try:
            if self.flag == self.SSDFLAG:
                logger.info(f"{self.SSDFLAG} ssd_webloan started")
                ssd = cfd_hd_be_overdue()
                ssd.p_phone = self.phone
                ssd.p_cycle = self.SSDWEBLOANCYCLE
                ssd.CODE = "200"
                ssd.phone = self.phone
                count = len(res.get("RESULTS",[{},{}])[1].get("DATA",[]))
                ssd.COUNTS = str(count)
                money = ""
                if count > 0:
                    money = res.get("RESULTS", [{}, {}])[1].get("DATA", [])[0].get("APPLICATIONAMOUNT","")
                ssd.MONEY = money
                ssd.PROVINCE = res.get("PROVINCE","")
                ssd.CITY = res.get("CITY","")
                ssd.save(using=self.SSDDB)
                logger.info(f"{self.SSDFLAG} ssd_webloan ended")
        except:
            logger.error("ssd_webloan",exc_info=True)
            return self.FAILED
        return self.SUCCESS

    def main(self):
        # add new
        a = self.hd_blackList()
        b = self.hd_blackList_detail()
        c = self.hd_illegal_info()
        d = self.hd_operator_rz()
        e = self.hd_webloan()
        f = self.hd_webloandetail()
        for adict in [a,b,c,d,e,f]:
            for code,msg in adict.items():
                if code == -1:
                    return self.FAILED
        new_msg = {"retcode": 0, "retmessage": "helpme succeed"}
        return new_msg
if __name__ == "__main__":
    m = hd_interface()
    m.hdAccountInfo = dict(
        AppID = "54411D08WDD64W44AAWB481W02113C17C493",
        AppSecret = "F64C3480L7B71L428ALB250LA3C5F41A70A7",
        Key = "276E8FE1H1E8BH4B6AHA1F4HEEC1029621FA",
    )
    m.name = "陈大磊"
    m.idcard = "340323198812020812"
    m.token = "DLXJD2017101000009"
    m.phone = "17717625664"
    m.hd_blackList()
    m.hd_blackList_detail()
    m.hd_illegal_info()
    m.hd_operator_rz()
    m.hd_webloan()
    m.hd_webloandetail()
