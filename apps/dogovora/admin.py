from django.contrib import admin

from apps.dogovora.models import DogovorIndi


@admin.register(DogovorIndi)
class DogovorAdmin(admin.ModelAdmin):
    list_display = ['tip_dogovora', 'nomer_dogovora', 'froze', 'author', 'published']
    search_fields = ('nomer_dogovora',)
    list_filter = ('tip_dogovora',)