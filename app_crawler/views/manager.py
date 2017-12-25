class Manager:
    compliteJson = {"retcode":0}
    classNum_empty = {"retcode":-1,"retmessage":""}
    success = {"retcode":0,"retmessage":"succeed"}
    flag = "flag"
    SSD_flag_val = "SSD"
    HM_flag_val = "HM"
    post_idcard = "idcard"
    post_name = "name"
    post_phone = "phone"
    post_token = "token"
    post_seqId = "seqId"
    right_style = {
        flag:"SSD/HM",
        post_idcard:"",
        post_name:"",
        post_phone:"",
        post_token:"",
    }
    illegal_request_resp = {"retcode":-1,
                            "retmessage":"only accept post method",
                            "rightStyle":right_style}
    hdAccountInfo = dict(
        AppID="54411D08WDD64W44AAWB481W02113C17C493",
        AppSecret="F64C3480L7B71L428ALB250LA3C5F41A70A7",
        Key="276E8FE1H1E8BH4B6AHA1F4HEEC1029621FA",
    )