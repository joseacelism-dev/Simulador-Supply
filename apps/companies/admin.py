from django.contrib import admin

from .models import Company, CompanyType


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "company_type", "city", "country", "difficulty")
    search_fields = ("name", "owner__username", "city", "country")
    list_filter = ("company_type", "difficulty", "country")

