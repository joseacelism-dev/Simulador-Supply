from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "segment", "city", "country", "expected_service_level")
    search_fields = ("name", "company__name", "city", "country")
    list_filter = ("company", "segment", "country")

