from app_crawler.storage.huadao.infos_emd008 import EMD008

def infos_emd008_test():
    e = EMD008(data=data1,idcard="13131314",phone="1111111111",name="13131314",db_name="helpMe")
    e.main()


data1 = {
    "CODE": "200",
    "PHONE": "1890215****",
    "PROVINCE": "北京",
    "CITY": "北京",
    "RESULTS": []
}

data = {
    "CODE":"200",
    "PHONE":"1890215****",
    "PROVINCE":"北京",
    "CITY":"北京",
    "RESULTS":[
        {
            "TYPE":"EMR002",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_111604 ",
                    "REGISTERTIME":"2016/3/14 0:00:00"
                },
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_111605 ",
                    "REGISTERTIME":"2016/3/14 0:00:00"
                },
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_111602 ",
                    "REGISTERTIME":"2016/3/14 0:00:00"
                }
            ]
        },
        {
            "TYPE":"EMR004",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_106744 ",
                    "APPLICATIONTIME":"2016/3/14 0:00:00",
                    "APPLICATIONAMOUNT":"0W~0.2W",
                    "APPLICATIONRESULT":"yes"
                },
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_106745 ",
                    "APPLICATIONTIME":"2016/3/14 0:00:00",
                    "APPLICATIONAMOUNT":"0W~0.2W",
                    "APPLICATIONRESULT":"yes"
                },
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_106746 ",
                    "APPLICATIONTIME":"2016/3/14 0:00:00",
                    "APPLICATIONAMOUNT":"0W~0.2W",
                    "APPLICATIONRESULT":"yes"
                }
            ]
        },
        {
            "TYPE":"EMR007",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_111604 ",
                    "LOANLENDERSTIME":"2016/3/14 0:00:00",
                    "LOANLENDERSAMOUNT":"0W~0.2W"
                },
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_111603 ",
                    "LOANLENDERSTIME":"2016/3/14 0:00:00",
                    "LOANLENDERSAMOUNT":"0W~0.2W"
                },
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_111602 ",
                    "LOANLENDERSTIME":"2016/3/14 0:00:00",
                    "LOANLENDERSAMOUNT":"0W~0.2W"
                }
            ]
        },
        {
            "TYPE":"EMR009",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "P_TYPE":"1",
                    "PLATFORMCODE":" EM_121900 ",
                    "REJECTIONTIME":"2016/3/14 0:00:00"
                },
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_121901 ",
                    "REJECTIONTIME":"2016/3/14 0:00:00"
                },
                {
                    "P_TYPE":"2",
                    "PLATFORMCODE":" EM_121902 ",
                    "REJECTIONTIME":"2016/3/14 0:00:00"
                }
            ]
        },
        {
            "TYPE":"EMR012",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "PLATFORM":" EM_121900 ",
                    "COUNTS":"284",
                    "MONEY":"0W~0.2W",
                    "D_TIME":"2016-04-10"
                },
                {
                    "PLATFORM":" EM_106744 ",
                    "COUNTS":"12",
                    "MONEY":"0W~0.2W",
                    "D_TIME":"2016-04-10"
                },
                {
                    "PLATFORM":" EM_121905 ",
                    "COUNTS":"60",
                    "MONEY":"0W~0.2W",
                    "D_TIME":"2016-04-10"
                }
            ]
        },
        {
            "TYPE":"EMR013",
            "CYCLE":"2015-07-11--2016-07-11",
            "DATA":[
                {
                    "PLATFORM":" EM_111602 ",
                    "MONEY":"0W~0.2W"
                }
            ]
        }
    ]
}

