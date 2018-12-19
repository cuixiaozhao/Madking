#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# 项目名称:MadKing
# 文件名称:urls.py
# 用户名:TQTL
# 创建时间:2018/12/18 19:16

from django.conf.urls import url
from apps.assets import views

urlpatterns = [
    url(r'report/asset_with_no_asset_id/$', views.asset_with_no_asset_id,name='acquire_asset_id'),
]
