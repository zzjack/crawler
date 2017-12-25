import json
from suds.client import Client
import traceback
from crawler.settings import logger
from app_crawler import models
from app_crawler.models import hd_token,hd_tokenwebloan
from app_crawler.storage.huadao.manager import TokenConf

# 2017/10/24 modify by zzjack
# four functions is combined a class,and ensure the return_value is uniform

class tokenUpdate(TokenConf):
    def main(self)->dict:
        try:
            del_msg,gs_msg = self.del_twoToken(),self.get_storage_twoToken()
            msg = f"{del_msg}{gs_msg}"
            if msg != "":
                self.runres["retcode"] = -1
                self.runres["retmessage"] = msg
                return self.runres
        finally:
            return self.runres

    def get_storage_twoToken(self)->str:
        msg = ""
        t_token,effective,t_err = self.get_token(self.t,self.t_appid,self.t_appsecret,self.t_key)
        t2_token,effective,t2_err = self.get_token(self.t2,self.t2_appid,self.t2_appsecret,self.t2_key)
        if t_err == "" and t2_err == "":
            self.insert_Token(self.t,t_token,effective)
            self.insert_Token(self.t2,t2_token,effective)
        else:
            msg = f"{t_err}{t2_err}"
        return msg

    def del_twoToken(self)->str:
        t_msg = self.deltoken(self.t)
        t2_msg = self.deltoken(self.t2)
        return f"{t_msg}{t2_msg}"
    def deltoken(self,table:str)-> str:
        msg = ""
        try:
            if table == self.t:
                hd_token.objects.using("token").all().delete()
            elif table == self.t2:
                # t = hd_tokenwebloan()
                # t.delete(using="token")
                hd_tokenwebloan.objects.using("token").all().delete()
            logger.info(f"{table} delete old token")
        except:
            logger.error("del error",exc_info=True)
            msg = traceback.format_exc()
        return msg
    def insert_Token(self,table: str, ret: str,effective:str):
        if table == self.t:
            t = models.hd_token()
            t.token = ret
            t.effctive = effective
            t.save(using="token")
        elif table == self.t2:
            t = models.hd_tokenwebloan()
            t.token = ret
            t.effctive = effective
            t.save(using="token")
        logger.info(f"{table} insert a new token {ret},effective {effective}")
    def get_token(self,table:str,appid:str,appsecret:str,key:str)->tuple:
        err = ""
        token = ""
        effective = ""
        res = ""
        try:
            client = Client(self.url)
            res = client.service.GetACCESS_TOKEN(AppID=appid, AppSecret=appsecret, Key=key)
            parseRes = json.loads(res)
            access_token = parseRes["access_token"]
            effective = parseRes["Effective"]
            token = access_token
        except:
            logger.error("update token",exc_info=True)
            err =  f"get {table} data error"
        return (token,effective,err)

if __name__=="__main__":
    t = tokenUpdate()
    t.main()