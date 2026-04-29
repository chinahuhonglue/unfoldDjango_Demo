from django.db import models
from simple_history.models import HistoricalRecords


class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ("server", "服务器"),
        ("workstation", "终端"),
        ("network", "网络设备"),
        ("app", "应用系统"),
    ]

    name = models.CharField("资产名称", max_length=100, unique=True)
    ip_address = models.GenericIPAddressField("IP地址", protocol="both", unpack_ipv4=True)
    asset_type = models.CharField("资产类型", max_length=20, choices=ASSET_TYPE_CHOICES, default="server")
    owner = models.CharField("负责人", max_length=50, blank=True)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "资产"
        verbose_name_plural = "资产"

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class Vulnerability(models.Model):
    LEVEL_CHOICES = [
        ("low", "低危"),
        ("medium", "中危"),
        ("high", "高危"),
        ("critical", "严重"),
    ]
    STATUS_CHOICES = [
        ("open", "待处理"),
        ("processing", "处理中"),
        ("closed", "已修复"),
    ]

    title = models.CharField("漏洞标题", max_length=200)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="vulnerabilities", verbose_name="关联资产")
    cve_id = models.CharField("CVE编号", max_length=30, blank=True)
    level = models.CharField("风险等级", max_length=10, choices=LEVEL_CHOICES, default="medium")
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default="open")
    description = models.TextField("漏洞描述", blank=True)
    discovered_at = models.DateTimeField("发现时间", auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "漏洞"
        verbose_name_plural = "漏洞"

    def __str__(self):
        return self.title


class SecurityAlert(models.Model):
    ALERT_LEVEL_CHOICES = [
        ("info", "信息"),
        ("warning", "警告"),
        ("danger", "高危"),
    ]

    title = models.CharField("告警标题", max_length=200)
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联资产")
    level = models.CharField("告警等级", max_length=10, choices=ALERT_LEVEL_CHOICES, default="warning")
    source = models.CharField("告警来源", max_length=100, blank=True)
    detail = models.TextField("告警详情", blank=True)
    created_at = models.DateTimeField("告警时间", auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "安全告警"
        verbose_name_plural = "安全告警"

    def __str__(self):
        return self.title