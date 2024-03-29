from django.contrib import admin

from apps.dogovora.models import DogovorIndi, DogovorEntry


@admin.register(DogovorIndi)
class DogovorAdmin(admin.ModelAdmin):
    list_display = ['tip_dogovora', 'nomer_dogovora', 'froze', 'published']
    search_fields = ('nomer_dogovora',)
    list_filter = ('tip_dogovora',)


@admin.register(DogovorEntry)
class DogovorEntryAdmin(admin.ModelAdmin):
    list_display = ['tip_dogovora', 'nomer_dogovora', 'froze', 'published']
    search_fields = ('nomer_dogovora',)
    list_filter = ('tip_dogovora',)
