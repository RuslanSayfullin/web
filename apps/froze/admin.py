from django.contrib import admin
from apps.froze.models import Froze, Client


@admin.register(Froze)
class FrozeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'client', 'type_production', 'created_at', 'status',)    # Поля, которые отображаются в панели администратора
    list_display_links = ('id', 'client')   # Поля, которые открывают заявку в панели администратора
    search_fields = ('id', 'uuid',)     # Поля, по которым можно выполнять поиск


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')  # Поля, которые отображаются в панели администратора
    list_display_links = ('id', 'name')     # Поля, которые открывают заявку в панели администратора
    search_fields = ('id', 'name',)         # Поля, по которым можно выполнять пойск
