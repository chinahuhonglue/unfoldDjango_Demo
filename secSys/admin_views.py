from datetime import timedelta

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from data.models import Asset, Vulnerability, SecurityAlert


@staff_member_required
def security_dashboard(request):
    now = timezone.now()
    day_ago = now - timedelta(hours=24)

    vul_level_map = {
        "low": "低危",
        "medium": "中危",
        "high": "高危",
        "critical": "严重",
    }

    alert_level_map = {
        "info": "信息",
        "warning": "警告",
        "danger": "高危",
    }

    vul_level_qs = (
        Vulnerability.objects.values("level")
        .annotate(total=Count("id"))
        .order_by("level")
    )
    alert_level_qs = (
        SecurityAlert.objects.values("level")
        .annotate(total=Count("id"))
        .order_by("level")
    )

    vul_by_level = [
        {
            "key": item["level"],
            "name": vul_level_map.get(item["level"], item["level"]),
            "total": item["total"],
        }
        for item in vul_level_qs
    ]

    alert_by_level = [
        {
            "key": item["level"],
            "name": alert_level_map.get(item["level"], item["level"]),
            "total": item["total"],
        }
        for item in alert_level_qs
    ]

    context = {
        # 关键：注入 admin 上下文，页面嵌入后台壳子
        **admin.site.each_context(request),
        "title": "安全态势总览",
        "subtitle": "Security Dashboard",
        "asset_total": Asset.objects.count(),
        "asset_active": Asset.objects.filter(is_active=True).count(),
        "vul_total": Vulnerability.objects.count(),
        "vul_open": Vulnerability.objects.filter(status="open").count(),
        "alert_total": SecurityAlert.objects.count(),
        "alert_24h": SecurityAlert.objects.filter(created_at__gte=day_ago).count(),
        "vul_by_level": vul_by_level,
        "alert_by_level": alert_by_level,
    }
    return render(request, "admin/security_dashboard.html", context)