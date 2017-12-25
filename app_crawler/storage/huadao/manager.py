class HDInterfaceUrl:
    hdTokenUrl = "http://opensdk.emay.cn:9099/HD_GetAccess_Token.asmx/GetACCESS_TOKEN"
    hdTokenWebloanUrl = "http://opensdk.emay.cn:9099/HD_GetAccess_Token.asmx/GetACCESS_TOKEN"
    hdBlackListUrl = "http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx/Get_EMW_BlackFuzzy_CX"
    hdEMD008Url = "http://opensdk.emay.cn:9099/MADE_API/emda_xdzh.asmx/GetEmda_xdzh_dt"
    hdIllegalInfoUrl = "http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx/Get_EMW_IllegalInfo_BLXXCX"
    hdOperatorRzUrl = "http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx/Get_EMW_Operator_RZ"

class TokenConf:
    runres = {
        "retcode":0,
        "retmessage":"token update success"
    }
    t = "hd_token"
    t2 = "hd_tokenwebloan"
    t_appid = '54411D08WDD64W44AAWB481W02113C17C493'
    t_appsecret = 'F64C3480L7B71L428ALB250LA3C5F41A70A7'
    t_key = '276E8FE1H1E8BH4B6AHA1F4HEEC1029621FA'
    t2_appid ='F016DC42W324CW44A4WB109W3111831914F2'
    t2_appsecret ='ACBE904DL036BL4EBBLB8A7L756C03D89BBE'
    t2_key = 'FBA9E271H1D9CH469AH92AAH159A3F0FEDB2'
    url = "http://opensdk.emay.cn:9099/HD_GetAccess_Token.asmx?wsdl"

class storageMsg:
    retcode_name = "retcode"
    retcode_success = 0
    retcode_failed = -1
    retmessage_name = "retmessage"
    retmessage_success = "succeed"
    retmessage_failed = "failed,detect log to know more details"
    SUCCESS = {
        retcode_name:retcode_success, retmessage_name: retmessage_success
    }
    FAILED = {
        retcode_name:retcode_failed, retmessage_name:retmessage_failed
    }