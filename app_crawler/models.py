from django.db import models

# EMW025 黑名单模糊汇总查询
# blackList
class Hd_EMW025(models.Model):
    name = models.CharField(max_length=50)
    idcard = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    ori_data = models.TextField()
    flag = models.CharField(max_length=20)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "appcrawler_hd_emw025"


# EMD008 信贷整合接口
# webloan/webloandetai/
class Hd_EMD008(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "appcrawler_hd_emd008"


# EMR012 逾期平台详情查询
# blackList_detail
class Hd_EMR012(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name
    class Meta:
        db_table = "appcrawler_hd_emr012"


# EMW018 不良信息查询
# illegal_info
# http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx?op=Get_EMW_IllegalInfo_BLXXCX
class Hd_EMW018(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name
    class Meta:
        db_table = "appcrawler_hd_emw018"


# EMW005运营商实名认证
# operator_rz
# http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx?op=Get_EMW_Operator_RZ
class Hd_EMW005(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name
    class Meta:
        db_table = "appcrawler_hd_emw005"


# EMR002 信贷平台注册详情，统计这个接口的数量
class Hd_EMR002(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name
    class Meta:
        db_table = "appcrawler_hd_emr002"


# EMR003 贷款申请次数
class Hd_EMR003(models.Model):
    name = models.CharField(max_length=50,help_text='name')
    idcard = models.CharField(max_length=30,help_text='identity card')
    phone = models.CharField(max_length=30,help_text='phone number')
    ori_data = models.TextField(help_text='原始数据')
    flag = models.CharField(max_length=20,help_text='1随时贷；2海米')
    ctime = models.DateTimeField(auto_now_add=True)
    def __str__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.name
    class Meta:
        db_table = "appcrawler_hd_emr003"

#bsd_blacklisthitnum
class bsd_blacklisthitnum(models.Model):
    request_id = models.AutoField(db_column="request_id",primary_key=True,auto_created=True,help_text="")
    seq_id = models.CharField(db_column="seq_id",max_length=40)
    p_person_id = models.CharField(db_column="p_person_id",max_length=50)
    black_risk_type = models.CharField(db_column="black_risk_type",max_length=50)
    black_hit_count = models.CharField(db_column="black_hit_count",max_length=50)
    CODE = models.CharField(db_column="CODE",max_length=50)
    data_source = models.CharField(db_column="data_source",max_length=10)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_blacklisthitnum"

#
class bsd_loanapplicationnum(models.Model):
    request_id = models.AutoField(db_column="request_id",primary_key=True)
    seq_id = models.CharField(db_column="seq_id", max_length=40)
    p_Phone = models.CharField(db_column="p_Phone",max_length=50)
    p_cycle = models.CharField(db_column="p_cycle",max_length=50)
    p_Platform = models.CharField(db_column="p_Platform",max_length=50)
    CODE = models.CharField(db_column="CODE", max_length=50)
    CYCLE = models.CharField(db_column="CYCLE",max_length=50)
    LOANNUM = models.CharField(db_column="LOANNUM",max_length=50)
    data_source = models.CharField(db_column="data_source",max_length=10)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_loanapplicationnum"

class bsd_hy_illegalinfo_summary(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    seq_id = models.CharField(db_column="seq_id", max_length=40)
    query_id = models.CharField(db_column="query_id",max_length=50)
    p_person_id = models.CharField(db_column="p_person_id",max_length=50)
    p_person_name = models.CharField(db_column="p_person_name", max_length=20)
    CODE = models.CharField(db_column="CODE", max_length=50)
    result = models.CharField(db_column="result", max_length=50)
    resultdesc = models.CharField(db_column="resultdesc", max_length=50)
    MESSAGE = models.CharField(db_column="MESSAGE", max_length=100)
    data_source = models.CharField(db_column="data_source", max_length=10)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_illegalinfo_summary"

class bsd_hy_blacklist_hit_summary(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_person_id = models.CharField(db_column="p_person_id", max_length=50)
    p_person_name = models.CharField(db_column="p_person_name", max_length=20)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    query_id = models.CharField(db_column="query_id", max_length=50)
    status = models.CharField(db_column="status", max_length=50)
    black_risk_type = models.CharField(db_column="black_risk_type", max_length=50)
    black_hit_count = models.CharField(db_column="black_hit_count", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_blacklist_hit_summary"

class cfd_hd_huifamohufact(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_idcode = models.CharField(db_column="p_idcode", max_length=50)
    status = models.CharField(db_column="status", max_length=50)
    totalnumber = models.CharField(db_column="totalnumber", max_length=50)
    casenumber = models.CharField(db_column="casenumber", max_length=50)
    zhixinnumber = models.CharField(db_column="zhixinnumber", max_length=50)
    taxnumber = models.CharField(db_column="taxnumber", max_length=50)
    cuiqiannumber = models.CharField(db_column="cuiqiannumber", max_length=50)
    kaitinnumber = models.CharField(db_column="kaitinnumber", max_length=50)
    othernumber = models.CharField(db_column="othernumber", max_length=50)
    shenpannumber = models.CharField(db_column="shenpannumber", max_length=50)
    wangdainumber = models.CharField(db_column="wangdainumber", max_length=50)
    success = models.CharField(db_column="success", max_length=50)
    cfd_module = models.CharField(db_column="cfd_module", max_length=50,default="")
    key_id = models.CharField(db_column="keyid", max_length=50)
    datatype = models.CharField(db_column="datatype", max_length=50)
    title = models.CharField(db_column="title", max_length=50)
    datatime = models.CharField(db_column="datatime", max_length=50)
    description = models.CharField(db_column="description", max_length=1000)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "cfd_hd_huifamohufact"

class cfd_hd_IllegalInfo_BLXXCX(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_person_id = models.CharField(db_column="p_person_id", max_length=50)
    p_person_name = models.CharField(db_column="p_person_name", max_length=20)
    CODE = models.CharField(db_column="CODE", max_length=50)
    result = models.CharField(db_column="result", max_length=50)
    resultdesc = models.CharField(db_column="resultdesc", max_length=50)
    MESSAGE = models.CharField(db_column="MESSAGE", max_length=100)
    data_source = models.CharField(db_column="data_source", max_length=10)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "cfd_hd_IllegalInfo_BLXXCX"


class bsd_hy_operator_rz(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_person_id = models.CharField(db_column="p_person_id", max_length=50)
    p_person_name = models.CharField(db_column="p_person_name", max_length=20)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    query_id = models.CharField(db_column="query_id", max_length=50)
    CODE = models.CharField(db_column="CODE", max_length=50)
    person_id = models.CharField(db_column="person_id", max_length=50)
    person_name = models.CharField(db_column="person_name", max_length=20)
    phone = models.CharField(db_column="phone", max_length=50)
    result = models.CharField(db_column="result", max_length=50)
    resultdesc = models.CharField(db_column="resultdesc", max_length=50)
    channel_name = models.CharField(db_column="channel_name", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_operator_rz"


class cfd_hd_operator_rz(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_person_id = models.CharField(db_column="p_person_id", max_length=50)
    p_person_name = models.CharField(db_column="p_person_name", max_length=20)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    query_id = models.CharField(db_column="query_id", max_length=50)
    CODE = models.CharField(db_column="CODE", max_length=50)
    person_id = models.CharField(db_column="person_id", max_length=50)
    person_name = models.CharField(db_column="person_name", max_length=20)
    phone = models.CharField(db_column="phone", max_length=50)
    result = models.CharField(db_column="result", max_length=50)
    resultdesc = models.CharField(db_column="resultdesc", max_length=50)
    channel_name = models.CharField(db_column="channel_name", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "cfd_hd_operator_rz"


class cfd_hd_be_overdue(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    p_cycle = models.CharField(db_column="p_cycle", max_length=50)
    CODE = models.CharField(db_column="CODE", max_length=50)
    phone = models.CharField(db_column="phone", max_length=50)
    COUNTS = models.CharField(db_column="COUNTS", max_length=50)
    MONEY = models.CharField(db_column="MONEY", max_length=50)
    PROVINCE = models.CharField(db_column="PROVINCE", max_length=50)
    CITY = models.CharField(db_column="CITY", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "cfd_hd_be_overdue"


class hd_token(models.Model):
    token = models.CharField(db_column="token",max_length=200)
    effctive = models.CharField(db_column="effctive",max_length=50)
    class Meta:
        db_table = "hd_token"


class hd_tokenwebloan(models.Model):
    token = models.CharField(db_column="token",max_length=200)
    effctive = models.CharField(db_column="effctive",max_length=50)
    class Meta:
        db_table = "hd_tokenwebloan"


class cfd_hd_creditregistration(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    p_cycle = models.CharField(db_column="p_cycle", max_length=50)
    p_Platform = models.CharField(db_column="p_Platform", max_length=50)
    CODE = models.CharField(db_column="CODE", max_length=50)
    CYCLE = models.CharField(db_column="CYCLE", max_length=50)
    REGISTERNUM = models.CharField(db_column="REGISTERNUM", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "cfd_hd_creditregistration"


class cfd_hy_webloan_detail(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    query_id = models.CharField(db_column="query_id", max_length=50)
    period_name = models.CharField(db_column="period_name", max_length=50)
    period_months = models.IntegerField(db_column="period_months")
    class_name = models.CharField(db_column="class_name", max_length=50)
    class_count = models.IntegerField(db_column="class_count")
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "cfd_hy_webloan_detail"


class bsd_hy_blacklist_hit_detail(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_person_id = models.CharField(db_column="p_person_id", max_length=20)
    query_id = models.CharField(db_column="query_id", max_length=50)
    status = models.CharField(db_column="status", max_length=50)
    black_risk_type = models.CharField(db_column="black_risk_type", max_length=50)
    overdue_amount_most = models.CharField(db_column="overdue_amount_most", max_length=50)
    overdue_count = models.CharField(db_column="overdue_count", max_length=50)
    overdue_days_most = models.CharField(db_column="overdue_days_most", max_length=50)
    overdue_time_latest = models.CharField(db_column="overdue_time_latest", max_length=50)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_blacklist_hit_detail"


class bsd_hy_webloan(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    p_name = models.CharField(db_column="p_name", max_length=50)
    p_phone = models.CharField(db_column="p_phone", max_length=50)
    p_id_card = models.CharField(db_column="p_id_card", max_length=50)
    result_code = models.CharField(db_column="result_code", max_length=20)
    product_res_code = models.CharField(db_column="product_res_code", max_length=20)
    query_id = models.CharField(db_column="query_id", max_length=50)
    query_time = models.CharField(db_column="query_time", max_length=30)
    ttl_hit_count = models.IntegerField(db_column="ttl_hit_count")
    ttl_hit_pname = models.CharField(db_column="ttl_hit_pname", max_length=200)
    risk_level = models.CharField(db_column="risk_level", max_length=10)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_webloan"

class bsd_hy_webloan_detail(models.Model):
    request_id = models.AutoField(db_column="request_id", primary_key=True)
    query_id = models.CharField(db_column="query_id", max_length=50)
    period_name = models.CharField(db_column="period_name", max_length=30)
    period_months = models.IntegerField(db_column="period_months")
    class_name = models.CharField(db_column="class_name", max_length=20)
    class_count = models.IntegerField(db_column="class_count")
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bsd_hy_webloan_detail"


class zhengxin91_crawler_log(models.Model):
    name = models.CharField(db_column="name",max_length=50)
    idcard = models.CharField(db_column="idcard",max_length=100)
    ctime = models.DateTimeField(auto_now=True)
    status = models.CharField(db_column="status",max_length=10) #suceess complete 1,or 0
    verify_res = models.CharField(db_column="verify_res",max_length=10)
    request_res = models.CharField(db_column="request_res",max_length=10) #transform res then send
    parse_res = models.CharField(db_column="parse_res",max_length=10) #parse response
    insert_res = models.CharField(db_column="insert_res",max_length=10)
    note = models.CharField(db_column="note",max_length=200)
    class Meta:
        db_table = "zhengxin91_crawler_log"


class zhengxin91_content(models.Model):
    name = models.CharField(db_column="name", max_length=50)
    idcard = models.CharField(db_column="idcard", max_length=100)
    ctime = models.DateTimeField(auto_now=True)
    ctime_stamp = models.IntegerField(db_column="ctime_stamp")
    trx_no = models.CharField(db_column="trx_no",max_length=100)
    status_code = models.CharField(db_column="status_code", max_length=20)
    err_msg = models.CharField(db_column="err_msg",max_length=300)
    borrow_type = models.IntegerField(db_column="borrow_type")
    borrow_status = models.IntegerField(db_column="borrow_status")
    borrow_amount = models.IntegerField(db_column="borrow_amount")
    contract_data = models.CharField(db_column="contract_data",max_length=50)
    loan_period = models.IntegerField(db_column="loan_period")
    repay_state = models.IntegerField(db_column="repay_state")
    arrears_amount = models.IntegerField(db_column="arrears_amount")
    company_code = models.CharField(db_column="company_code",max_length=500)
    class Meta:
        db_table = "zhengxin91_content"


class zhengxin91_ori_data(models.Model):
    name = models.CharField(db_column="name",max_length=50)
    idcard = models.CharField(db_column="idcard",max_length=100)
    ctime = models.DateTimeField(auto_now=True)
    flag = models.CharField(max_length=20)
    status_code = models.CharField(db_column="status_code",max_length=20)
    ori_data = models.TextField(db_column="ori_data")
    class Meta:
        db_table = "zhengxin91_ori_data"


class ZhengXin91ShareLog(models.Model):
    name = models.CharField(db_column="name",max_length=50)
    idcard = models.CharField(db_column="idcard",max_length=100)
    ctime = models.DateTimeField(auto_now=True)
    status = models.CharField(db_column="status",max_length=10) #suceess complete 1,or 0
    verify_rcv = models.CharField(db_column="verify_receive",max_length=10)
    parse_res = models.CharField(db_column="parse_res", max_length=10)
    not_empty = models.CharField(db_column="not_empty", max_length=10)
    query_table = models.CharField(db_column="query_table",max_length=10) #transform res then send
    trans_res = models.CharField(db_column="trans_res",max_length=10) #parse response
    save_cache = models.CharField(db_column="save_cache",max_length=10)
    note = models.CharField(db_column="note",max_length=200)
    class Meta:
        db_table = "zhengxin91_share_log"


class ZhengXin91ShareOriData(models.Model):
    name = models.CharField(db_column="name",max_length=50)
    idcard = models.CharField(db_column="idcard",max_length=100)
    ctime = models.DateTimeField(auto_now=True)
    status_code = models.CharField(db_column="status_code",max_length=20)
    ori_data = models.TextField(db_column="ori_data")
    ctime_stamp = models.IntegerField(db_column="ctime_stamp")
    class Meta:
        db_table = "zhengxin91_share_ori_data"


class JkLoanApply(models.Model):
    uid = models.IntegerField(db_column="uid")
    apply_id = models.CharField(db_column="apply_id", max_length=215)
    product_id = models.IntegerField(db_column="product_id")
    product_name = models.CharField(db_column="product_name", max_length=32)
    name = models.CharField(db_column="name",max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    amount = models.DecimalField(db_column="amount",max_digits=20,decimal_places=2)
    province = models.CharField(db_column="province", max_length=20)
    city = models.CharField(db_column="city", max_length=20)
    district = models.CharField(db_column="district", max_length=20)
    invitation_code = models.CharField(db_column="invitation_code", max_length=215)
    tenant = models.CharField(db_column="tenant",max_length=20)
    status = models.IntegerField(db_column="status")
    type = models.IntegerField(db_column="type")
    step = models.IntegerField(db_column="step")
    identity_id = models.CharField(db_column="identity_id",max_length=64)
    is_valid = models.IntegerField(db_column="is_valid")
    vaild_date = models.DateField(db_column="vaild_date")
    is_manual_audit = models.IntegerField(db_column="is_manual_audit")
    order_no = models.CharField(db_column="order_no",max_length=255)
    modify_time = models.DateField(db_column="modify_time")
    create_time = models.DateField(db_column="create_time")
    class Meta:
        db_table = "jk_loan_apply"

class JkUserLoanRecord(models.Model):
    uid = models.IntegerField(db_column="uid")
    amount = models.DecimalField(db_column="amount",max_digits=20,decimal_places=2)
    pay_time = models.DateTimeField(db_column="pay_time")
    class Meta:
        db_table = "jk_user_loan_record"

class HDEMD008Manager(models.Model):
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard", max_length=20)
    code = models.CharField(db_column="code",max_length=20)
    phone = models.CharField(db_column="phone",max_length=20)
    province = models.CharField(db_column="province",max_length=50)
    city = models.CharField(db_column="city",max_length=50)
    results = models.CharField(db_column="result",max_length=20)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_manager"

class HDEMD008EMR002(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard",max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform_code = models.CharField(db_column="platform_code",max_length=50)
    register_time = models.CharField(db_column="register_time",max_length=50)
    p_type = models.CharField(db_column="p_type",max_length=10)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr002"

class HDEMD008EMR004(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard",max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform_code = models.CharField(db_column="platform_code", max_length=50)
    application_time = models.CharField(db_column="application_time",max_length=50)
    application_amount = models.CharField(db_column="application_amount",max_length=50)
    application_result = models.CharField(db_column="application_result",max_length=50)
    p_type = models.CharField(db_column="p_type",max_length=10)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr004"

class HDEMD008EMR007(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard", max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform_code = models.CharField(db_column="platform_code", max_length=50)
    loan_lenders_time = models.CharField(db_column="loan_lenders_time",max_length=50)
    loan_lenders_amount = models.CharField(db_column="loan_lenders_amount",max_length=50)
    p_type = models.CharField(db_column="p_type",max_length=10)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr007"

class HDEMD008EMR009(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard", max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform_code = models.CharField(db_column="platform_code", max_length=50)
    rejection_time = models.CharField(db_column="rejection_time",max_length=50)
    p_type = models.CharField(db_column="p_type", max_length=10)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr009"

class HDEMD008EMR012(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard", max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform  = models.CharField(db_column="platform",max_length=50)
    counts = models.CharField(db_column="counts",max_length=20)
    money = models.CharField(db_column="money",max_length=50)
    d_time = models.CharField(db_column="d_time",max_length=30)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr012"

class HDEMD008EMR013(models.Model):
    emd_id = models.IntegerField(db_column="emd_id")
    name = models.CharField(db_column="name", max_length=20)
    mobile = models.CharField(db_column="mobile", max_length=20)
    idcard = models.CharField(db_column="idcard", max_length=20)
    cycle = models.CharField(db_column="cycle",max_length=50)
    platform = models.CharField(db_column="platform", max_length=50)
    money = models.CharField(db_column="money", max_length=50)
    mtime = models.DateTimeField(auto_now=True)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "hd_emd008_emr013"


















