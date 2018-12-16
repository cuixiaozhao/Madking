from django.db import models


# Create your models here.


class Asset(models.Model):
    """资产信息表"""
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')  # 资产的名称必须设置为唯一值，要不然没有意义！
    # 资产类型选项
    asset_type_choices = (
        ('server', '服务器'),
        ('networkDevice', '网络设备'),
        ('storageDevice', '存储设备'),
        ('securityDevice', '安全设备'),
        ('software', '软件资产'),
        # ('switch','交换机'),
        # ('router','路由器'),
        # ('firewall','防火墙'),
        # ('storage','存储设备'),
        # ('NLB','NetScaler'),
        # ('others','其他类'),
    )
    # ('wireless','无线AP'),
    asset_type = models.CharField(max_length=64, choices=asset_type_choices, default='server', verbose_name='资产类型')
    business_unit = models.ForeignKey('BusinessUnit', blank=True, null=True,
                                      verbose_name='业务线')  # blank和null均为True，一般都是并存！
    sn = models.CharField('资产SN号', max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory', blank=True, null=True, verbose_name='生产厂商')
    # model = models.ForeignKey('ProductModel', verbose_name='型号')
    # model = models.CharField('型号', max_length=128, blank=True, null=True)
    management_ip = models.GenericIPAddressField(blank=True,
                                                 null=True,
                                                 verbose_name='管理IP')  # 机器的远程管理卡IP或者纯外网的IP，所以没有写成unique=True；
    contract = models.ForeignKey('Contract', blank=True, null=True, verbose_name='合同')
    trade_date = models.DateField(blank=True, null=True, verbose_name='购买日期')
    expire_date = models.DateField(blank=True, null=True, verbose_name='过保日期')
    price = models.FloatField(blank=True, null=True, verbose_name='价格')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name='资产管理员')
    idc = models.ForeignKey('IDC', blank=True, null=True, verbose_name='IDC机房')
    # status = models.ForeignKey('Status', default=1, verbose_name='设备状态')
    # configuration = models.OneToOneField('Configuration', blank=True, null=True, verbose_name='配置管理')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')  # auto_now_add属性为自动创建;
    update_date = models.DateTimeField(blank=True, auto_now=True, verbose_name='更新时间')  # auto_now属性为每次更新，时间自动变化；

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)


class Server(models.Model):
    """服务器信息"""
    asset = models.OneToOneField(Asset, verbose_name='资产')  # 与资产表是’一对一‘的对应关系；
    sub_asset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),  # 使用数字或字母的原因是:节省字节空间；要具备这种思想，虽然节省的空间有限！
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name='')
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    created_by = models.CharField(choices=created_by_choices, max_length=32, default='auto', verbose_name='创建方式')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)  # 虚拟机的SN号码不容易抓取；
    # sn = models.CharField(max_length=128, unique = True,verbose_name='SN号')
    # management_ip = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'管理IP')
    # manufactory = models.ForeignKey(max_length=128, blank=True, null=True, verbose_name='制造商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    # 若有多个CPU，型号应该是一致的，故没有做ForeignKey；
    # nic = models.ManyToManyField('NIC',verbose_name='网卡列表')

    # Disk相关信息如下:
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='raid类型')
    # physical_disk_driver = models.ManyToManyField('Disk', blank=True, null=True, verbose_name='硬盘')
    # raid_adaptor = models.ManyToManyField('RaidAdaptor', blank=True, null=True, verbose_name='Raid卡')

    # Memory相关信息如下:
    # ram_capacity = models.IntegerField(blank=True, verbose_name='内存总大小GB')
    # ram = models.ManyToManyField('Memory', blank=True, null=True, verbose_name='内存配置')
    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发型版本')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作系统版本')

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        unique_together = ['sn', 'asset']

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


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
    sn = models.CharField('SN号', max_length=128)
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    manufactory = models.ForeignKey(max_length=128, blank=True, null=True, verbose_name='制造商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    # 若有多个CPU，CPU的型号应该是一致的，故没有做ForeignKey
    nic = models.ManyToManyField('NIC', verbose_name='网卡列表')
    raid_type = models.CharField('raid类型', max_length=512, blank=True, null=True)
    physical_disk_driver = models.ManyToManyField('Disk', blank=True, null=True, verbose_name='硬盘')
    raid_adapter = models.ManyToManyField('RaidAdaptor', blank=True, null=True, verbose_name='Raid卡')
    # Memory
    ram_capacity = models.IntegerField('内存总大小GB', blank=True)
    ram = models.ManyToManyField('Memory', blank=True, null=True, verbose_name='内存配置')
    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)


class SecurityDevice(models.Model):
    """安全设备"""
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name='服务器类型')

    def __str__(self):
        return self.asset.id


class NetworkDevice(models.Model):
    """网络设备"""
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, default=0, verbose_name='网络设备类型')
    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='VlanIP')
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')
    # sn = models.CharField('SN号', max_length=128, unique=True)
    # manufactory = models.CharField(max_length=128, blank=True, null=True, verbose_name='制造商')
    model = models.CharField(max_length=64, blank=True, null=True, verbose_name='型号')
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name='固件')
    port_num = models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')
    device_detail = models.TextField(blank=True, null=True, verbose_name='设置详细配置')

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name


class Software(models.Model):
    """软件资产（只存储花费买的软件）"""
    # os_types_choices = (
    #     (0, 'OS'),
    #     (1, '办公\开发软件'),
    #     (2, '业务软件'),
    # )
    license_num = models.IntegerField(verbose_name='授权数')
    # os_distribution_choices = (
    #      ('windows', 'Windows'),
    #      ('centos', 'CentOS'),
    #      ('ubuntu', 'Ubuntu'),
    #  )
    # type = models.CharField(choices=os_types_choices, max_length=64, help_text=u'eg. GNU/Linux', verbose_name='系统类型')
    # distribution = models.CharField(choices=os_distribution_choices, max_length=32, default='windows')
    version = models.CharField(max_length=64, help_text='eg. CentOS release 6.5 (Final)')

    # language_choices = (
    #     ('cn', u'中文'),
    #     ('en', u'英文'),
    # )
    # language = models.CharField(choices=language_choices, default='cn', max_length=64)
    # version = models.CharField(max_length=64, help_text='2.6.32-431.3.1.el6.x86_64')

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


class Disk(models.Model):
    """存储硬盘信息"""
    asset = models.ForeignKey('Asset')
    sn = models.CharField(max_length=128, blank=True, null=True,
                          verbose_name='SN号')  # 有时候硬盘的SN号码，脚本抓取不到；虚拟机虚拟出来的硬盘，SN更是不准确！
    slot = models.CharField(max_length=64, verbose_name='插槽位')
    # manufactory = models.CharField(max_length=64, blank=True, null=True,verbose_name='制造商')# 制造商存储在型号里面；
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='磁盘型号')
    capacity = models.FloatField(verbose_name='磁盘容量GB')
    disk_iface_choices = (
        ('sata', 'SATA'),
        ('sas', 'SAS'),
        ('scsi', 'SCSI'),
        ('ssd', 'SSD'),
    )  # IDE淘汰，不再存储；
    iface_type = models.CharField(max_length=64, choices=disk_iface_choices, default='SAS', verbose_name='接口类型')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')  # 硬盘可单独更新，遂存在时间
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')
    auto_create_fields = ['sn', 'slot', 'manufacotry', 'model', 'capacity', 'iface_type']  # 自动创建；

    class Meta:
        unique_together = ('server', 'slot')  # 联合唯一；
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    pass
