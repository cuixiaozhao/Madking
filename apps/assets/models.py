from django.db import models


# Create your models here.


class Asset(models.Model):
    """
    资产表
    """
    asset_type_choices = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('storagedevice', u'存储设备'),
        ('securitydevice', u'安全设备'),
        # ('switch',u'交换机'),
        # ('router',u'路由器'),
        # ('firewall',u'防火墙'),
        # ('storage',u'存储设备'),
        # ('NLB',u'NetScaler'),
        # ('wireless',u'无线AP'),
        ('software', u'软件资产'),
        # ('others',u'服务器'),
    )
    asset_type = models.CharField(choices=asset_type_choices, default='server', max_length=64)
    business_unit = models.ForeignKey('BusinessUnit', blank=True, null=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True, )
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', blank=True, null=True)
    # model = models.ForeignKey('ProductModel', verbose_name=u'型号')
    # model = models.CharField(u'型号', max_length=128, blank=True, null=True)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)  # 机器的远程管理卡IP或者纯外网IP，所以没有写成unique；
    contract = models.ForeignKey('Contract', blank=True, null=True, verbose_name=u'合同')
    trade_date = models.DateField(u'购买日期', blank=True, null=True)
    expire_date = models.DateField(u'过保日期', blank=True, null=True)
    price = models.FloatField(u'价格', blank=True, null=True)
    business_unit = models.ForeignKey('BusinessUnit', blank=True, null=True, verbose_name=u'资产管理员')
    tags = models.ManyToManyField('Tag', blank=True)
    admin = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name=u'资产管理员')
    idc = models.ForeignKey('IDC', blank=True, null=True, verbose_name=u'IDC机房')
    # status = models.ForeignKey('Status', default=1, verbose_name=u'设备状态')
    # configuration = models.OneToOneField('Configuration', blank=True, null=True, verbose_name=u'配置管理')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Server(models.Model):
    """服务器信息"""
    asset = models.OneToOneField(Asset)


class BusinessUnit(models.Model):
    """"""
    sub_asset_type_choices = (
        (0, 'PC服务器'),  # 使用数字，节省存储空间；
        (1, '刀片机'),
        (2, '小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128)
    management_ip = models.CharField(u'管理IP', max_length=64, blank=True, null=True)
    manufactory = models.ForeignKey(max_length=128, blank=True, null=True, verbose_name=u'制造商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'型号')
    # 若有多个CPU，CPU的型号应该是一致的，故没有做ForeignKey
    nic = models.ManyToManyField('NIC', verbose_name=u'网卡列表')
    raid_type = models.CharField(u'raid类型', max_length=512, blank=True, null=True)
    physical_disk_driver = models.ManyToManyField('Disk', blank=True, null=True, verbose_name=u'硬盘')
    raid_adapter = models.ManyToManyField('RaidAdaptor', blank=True, null=True, verbose_name=u'Raid卡')
    # Memory
    ram_capacity = models.IntegerField(u'内存总大小GB', blank=True)
    ram = models.ManyToManyField('Memory', blank=True, null=True, verbose_name=u'内存配置')
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)


class NetworkDevice(models.Model):
    """网络设备"""
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u'网络设备类型')
    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, unique=True)
    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    firmware = models.CharField('固件', blank=True, null=True)
    port_num = models.SmallIntegerField(u'端口个数', blank=True, null=True)
    device_detail = models.TextField(u'设备详细配置', blank=True, null=True)


class SecurityDevice(models.Model):
    """安全设备"""
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name=u'服务器类型')

    def __str__(self):
        return self.asset.id


class Software(models.Model):
    """软件资产（只存储花费买的软件）"""
    os_types_choices = (
        (0, 'OS'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )
    license_num = ""


class Disk(models.Model):
    """存储硬盘信息"""
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)  # 有时候硬盘的SN号码，抓取不到；虚拟机虚拟出来的硬盘，SN更是不准确！
    slot = models.CharField(u'插槽位', max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choices = (
        ('sata', 'SATA'),
        ('sas', 'SAS'),
        ('scsi', 'SCSI'),
        ('ssd', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choices, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    auto_create_fields = ['sn', 'slot', 'manufacotry', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ('server', 'slot')
        verbose_name = u'硬盘'
        verbose_name_plural = verbose_name
