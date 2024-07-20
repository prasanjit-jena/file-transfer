from django.contrib import admin
from .models import ProcessedData

@admin.register(ProcessedData)
class ProcessedDataAdmin(admin.ModelAdmin):
    list_display = ('id','year', 'month', 'category', 'clubbed_name', 'product', 'value')
    search_fields = ('year', 'month', 'category', 'clubbed_name', 'product')
