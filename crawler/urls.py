#!/usr/local/bin/python3.6
"""crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app_crawler.views.helpme import helpMe
from app_crawler.views.get_token import getHDToken
from app_crawler.views.ssd import SSDEMR003,\
    SSDEMW025,SSDPhoneRZlist,SSDIllegalInfo
from app_crawler.views import zhengxin91
from app_crawler.views import view_test


urlpatterns = [
    # 后台管理，待开发
    url(r'^admin/', admin.site.urls),
    # 海米
    url(r'^hd-helpme/',helpMe.as_view()),
    # 获取hd token
    url(r'^hd_token/',getHDToken),
    # four interfaces
    # 网络借贷
    url(r'^hd-webloan/', SSDEMR003.as_view()),
    # 黑名单模糊查询
    url(r'^hd-blacklist/', SSDEMW025.as_view()),
    # 运营商认证
    # 要返回一致不一致
    url(r'^hd-phone-rz/', SSDPhoneRZlist.as_view()),
    # 不良信息
    url(r'^hd-illegal-info/', SSDIllegalInfo.as_view()),
    # zhengxin91
    url(r'^zhengxin91/',zhengxin91.ZhengXin91Storage.as_view()),
    # zhengxin91shared
    url(r'^shared/zx91/',zhengxin91.ZhengXin91Share.as_view()),
    # test url
    # url(r'^test/emd008/',view_test.emd008_test),
]

