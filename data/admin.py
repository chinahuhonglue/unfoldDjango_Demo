from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from .models import Asset, Vulnerability, SecurityAlert


@admin.register(Asset)
class AssetAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = (
        "id",
        "name",
        "ip_address",
        "asset_type",
        "owner",
        "is_active",
        "updated_at",
    )
    list_filter = ("asset_type", "is_active", "created_at")
    search_fields = ("name", "ip_address", "owner")
    ordering = ("-updated_at",)

    list_per_page = 20
    date_hierarchy = "updated_at"
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("基础信息", {"fields": ("name", "ip_address", "asset_type", "owner", "is_active")}),
        ("时间信息", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Vulnerability)
class VulnerabilityAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ("id", "title", "asset", "cve_id", "level", "status", "discovered_at")
    list_filter = ("level", "status", "discovered_at")
    search_fields = ("title", "cve_id", "asset__name", "asset__ip_address")
    ordering = ("-discovered_at",)

    list_per_page = 20
    date_hierarchy = "discovered_at"
    list_editable = ("status",)
    autocomplete_fields = ("asset",)
    readonly_fields = ("discovered_at",)

    fieldsets = (
        ("漏洞信息", {"fields": ("title", "asset", "cve_id", "level", "status")}),
        ("详细信息", {"fields": ("description",)}),
        ("时间信息", {"fields": ("discovered_at",)}),
    )


@admin.register(SecurityAlert)
class SecurityAlertAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ("id", "title", "asset", "level", "source", "created_at")
    list_filter = ("level", "source", "created_at")
    search_fields = ("title", "source", "asset__name", "asset__ip_address")
    ordering = ("-created_at",)

    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("asset",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("告警信息", {"fields": ("title", "asset", "level", "source")}),
        ("详情", {"fields": ("detail",)}),
        ("时间信息", {"fields": ("created_at",)}),
    )