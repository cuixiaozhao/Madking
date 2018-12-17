#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# 项目名称:MadKing
# 文件名称:myauth.py
# 用户名:TQTL
# 创建时间:2018/12/17 17:59
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, Group, PermissionsMixin)

import django


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users Must Have an Email Address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            # token=token,
            # department=department,
            # tel=tel,
            # memo=memo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email,
                                password=password,
                                name=name,
                                # token=token,
                                # department=department,
                                # tel=tel,
                                # memo=memo,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(

        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    name = models.CharField(max_length=32)
    token = models.CharField(max_length=128, default=None, blank=True, null=True, verbose_name='token')
    department = models.CharField(max_length=32, default=None, blank=True, null=True)
    # business_unit = models.ManyToManyField('BusinessUnit')
    tel = models.CharField(max_length=32, default=None, blank=True, null=True, verbose_name='电话')
    mobile = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='手机')
    memo = models.TextField(blank=True, null=True, default=None, verbose_name='备注')
    date_joined = models.DateTimeField(blank=True, auto_now=True)
    # valid_begin = models.DateTimeField(blank=True, auto_now=True)
    # valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'token', 'department', 'tel', 'mobile', 'memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    objects = UserManager()
