from django.db import models
from apps.assets.myauth import UserProfile

from django.contrib.auth.models import User


# Create your models here.


# class UserProfile(User):
#     """"""
#     name = models.CharField(max_length=32, verbose_name='姓名')
#
#     class Meta:
#         super(User.Meta)
#         verbose_name = '用户配置'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class Asset(models.Model):
    """资产信息表"""
    # 资产类型选项；
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
        # ('wireless','无线AP'),
        # ('others','其他类'),
    )

    asset_type = models.CharField(max_length=64, choices=asset_type_choices, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')  # 资产的名称必须设置为唯一值，要不然没有意义！
    sn = models.CharField('资产SN号', max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory', blank=True, null=True, verbose_name='制造商')
    # model = models.ForeignKey('ProductModel', verbose_name='型号')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    # 机器的远程管理卡IP或者纯外网的IP，所以没有写成unique=True；
    management_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')
    contract = models.ForeignKey('Contract', blank=True, null=True, verbose_name='合同')
    trade_date = models.DateField(blank=True, null=True, verbose_name='购买日期')
    expire_date = models.DateField(blank=True, null=True, verbose_name='过保修期')
    price = models.FloatField(blank=True, null=True, verbose_name='价格')
    # blank和null均为True，一般都是并存！
    business_unit = models.ForeignKey('BusinessUnit', blank=True, null=True, verbose_name='所属业务线')
    admin = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name='资产管理员')
    idc = models.ForeignKey('IDC', blank=True, null=True, verbose_name='IDC机房')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')# ManyToManyField,null=True不需要写！
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
    """服务器设备信息"""
    asset = models.OneToOneField('Asset', verbose_name='资产')  # 与资产表是’一对一‘的对应关系；
    sub_asset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),  # 使用数字或字母的原因是:节省字节空间；要具备这种思想，虽然节省的空间有限！
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name='服务器类型', default=0)
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    created_by = models.CharField(max_length=32, choices=created_by_choices, default='auto', verbose_name='创建方式')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)  # 虚拟机的SN号码不容易抓取；
    # sn = models.CharField(max_length=128, unique = True,verbose_name='SN号')
    # management_ip = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'管理IP')
    # manufactory = models.ForeignKey(max_length=128, blank=True, null=True, verbose_name='制造商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    # 若有多个CPU，型号应该是一致的，故没有做ForeignKey；
    # nic = models.ManyToManyField('NIC',verbose_name='网卡列表')

    # Disk相关信息如下:
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')
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
        # together = ['sn', 'asset']

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


class SecurityDevice(models.Model):
    """安全设备"""
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, default=0, verbose_name='服务器类型')

    class Meta:
        verbose_name = '安全配置'
        verbose_name_plural = verbose_name

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

    sub_asset_types_choices = (
        (0, 'OS'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_types_choices, verbose_name='服务器类型', default=0)
    license_num = models.IntegerField(verbose_name='授权数')
    # os_distribution_choices = (
    #      ('windows', 'Windows'),
    #      ('centos', 'CentOS'),
    #      ('ubuntu', 'Ubuntu'),
    #  )
    # type = models.CharField(choices=os_types_choices, max_length=64, help_text=u'eg. GNU/Linux', verbose_name='系统类型')
    # distribution = models.CharField(choices=os_distribution_choices, max_length=32, default='windows')
    version = models.CharField(max_length=64, help_text='eg. CentOS release 6.5 (Final)', unique=True,
                               verbose_name='软件/系统版本')

    # language_choices = (
    #     ('cn', u'中文'),
    #     ('en', u'英文'),
    # )
    # language = models.CharField(choices=language_choices, default='cn', max_length=32)
    # version = models.CharField(max_length=64, help_text='2.6.32-431.3.1.el6.x86_64'，verbose_name = '版本号')

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


class CPU(models.Model):
    """CPU组件"""
    asset = models.OneToOneField('Asset')  # 一个机器的多块硬盘、内存可以是不同型号的，但是CPU必须都是一样的！所以是OneToOne；
    cpu_model = models.CharField(max_length=128, blank=True, verbose_name='CPU型号')
    cpu_count = models.SmallIntegerField(verbose_name='物理CPU个数')
    cpu_core_count = models.SmallIntegerField(verbose_name='CPU核心数')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cpu_model


class Ram(models.Model):
    """内存组件"""
    asset = models.ForeignKey('Asset')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    model = models.CharField(max_length=128, verbose_name='内存型号')
    slot = models.CharField(max_length=64, verbose_name='插槽')
    capacity = models.IntegerField(verbose_name='内存大小(MB)')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'slot')

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)


class Disk(models.Model):
    """硬盘组件"""
    asset = models.ForeignKey('Asset')
    # 有时候硬盘的SN号码，脚本抓取不到；虚拟机虚拟出来的硬盘，SN更是不准确！
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    slot = models.CharField(max_length=64, verbose_name='插槽位')
    # manufactory = models.CharField(max_length=64, blank=True, null=True,verbose_name='制造商')# 制造商存储在型号里面；
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='磁盘型号')
    capacity = models.FloatField(verbose_name='磁盘容量GB')
    disk_iface_choices = (
        ('sata', 'SATA'),
        ('sas', 'SAS'),
        ('scsi', 'SCSI'),
        ('ssd', 'SSD'),
    )  # IDE接口硬盘淘汰，不再存储；
    iface_type = models.CharField(max_length=64, choices=disk_iface_choices, default='SAS', verbose_name='接口类型')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')  # 硬盘可单独更新，遂存在时间
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新时间')
    auto_create_fields = ['sn', 'slot', 'manufacotry', 'model', 'capacity', 'iface_type']  # 自动创建；

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'slot')  # 联合唯一；

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    """网卡组件"""
    asset = models.ForeignKey('Asset')
    # server = models.ForeignKey('Server')
    name = models.CharField(max_length=54, blank=True, null=True, verbose_name='网卡名称')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='网卡型号')
    mac_address = models.CharField(max_length=64, unique=True, verbose_name='MAC')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')
    netmask = models.CharField(max_length=64, blank=True, null=True, verbose_name='网关')
    bonding = models.CharField(max_length=64, blank=True, null=True, verbose_name='绑定')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建日期')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = verbose_name
        # unique_together = ('asset_id', 'slot')
        unique_together = ('asset', 'mac_address')  # 虚拟机的MAC地址经常会重复，所以联合唯一；

    def __str__(self):
        return '%s:%s' % (self.asset, self.mac_address)

    auto_create_fields = ['name', 'sn', 'model', 'mac_address', 'ip_address', 'netmask', 'bonding']


class RaidAdaptor(models.Model):
    """Raid卡"""
    asset = models.ForeignKey('Asset')
    name = models.CharField(max_length=64, verbose_name='Raid卡名称')
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name='SN号')
    slot = models.CharField(max_length=64, verbose_name='插口')
    model = models.CharField(max_length=64, blank=True, null=True, verbose_name='型号')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建日期')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')

    class Meta:
        verbose_name = "Raid卡"
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'slot')

    def __str__(self):
        return self.name


class Manufactory(models.Model):
    """厂商"""
    manufactory = models.CharField(max_length=64, unique=True, verbose_name='厂商名称')
    support_num = models.CharField(max_length=32, blank=True, verbose_name='支持电话')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.manufactory


class BusinessUnit(models.Model):
    """业务线"""
    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线')
    # contact = models.ForeignKey('UserProfile',default=None,verbose_name='咨询')
    memo = models.TextField(max_length=64, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Contract(models.Model):
    """合同"""
    sn = models.CharField(max_length=128, unique=True, verbose_name='合同号')
    name = models.CharField(max_length=64, verbose_name='合同名称')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    price = models.IntegerField(verbose_name='合同金额')
    detail = models.TextField(blank=True, null=True, max_length='合同详细')
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(blank=True, verbose_name='license数量')
    create_date = models.DateField(blank=True, auto_now_add=True, verbose_name='创建日期')
    update_date = models.DateField(blank=True, auto_now=True, verbose_name='创建日期')

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签信息"""
    name = models.CharField(max_length=32, unique=True, verbose_name='Tag Name')
    creator = models.ForeignKey('UserProfile', verbose_name='创建人')
    create_date = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """事件日志"""
    name = models.CharField(max_length=128, verbose_name='事件名称')
    event_type_choices = (
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
        (7, '其他'),
    )
    event_type = models.SmallIntegerField(choices=event_type_choices, verbose_name='事件类型')
    asset = models.ForeignKey('Asset')
    component = models.CharField(max_length=256, blank=True, null=True, verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True, verbose_name='时间事件')
    user = models.ForeignKey('UserProfile', verbose_name='事件源')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background:orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background:yelllowgreen;">%s</span>'
        else:
            cell_html = '<span>%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = '事件类型'


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产SN号')
    asset_type_choices = (
        ('server', '服务器'),
        ('switch', '交换机'),
        ('router', '路由器'),
        ('firewall', '防火墙'),
        ('storage', '存储设备'),
        ('NLB', 'NetScaler'),
        ('wireless', '无线AP'),
        ('software', '软件资产'),
        ('others', '其他'),
    )

    asset_type = models.CharField(max_length=64, choices=asset_type_choices, blank=True, null=True, verbose_name='资产类型')
    manufactory = models.CharField(max_length=64, blank=True, null=True, verbose_name='厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='类型')
    ram_size = models.IntegerField(blank=True, null=True, verbose_name='内存大小(MB)')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU类型')
    cpu_count = models.IntegerField(blank=True, null=True, verbose_name='CPU数量')
    cpu_core_count = models.IntegerField(blank=True, null=True, verbose_name='CPU核心数量')
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name='发行版本')
    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统类型')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统版本')
    data = models.TextField(verbose_name='资产数据')
    date = models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')
    approved = models.BooleanField(default=False, verbose_name='已批准')
    approved_by = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name='批准人')
    approved_date = models.DateTimeField(blank=True, null=True, verbose_name='批准日期')

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sn
