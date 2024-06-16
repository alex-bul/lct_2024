# imagegen/admin.py
from django.contrib import admin
from .models import Session, Image


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')  # Ссылки для id и user


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'session',
        'channel',
        'product',
        'gender',
        'age',
        'cnt_tr_all_3m',
        'cnt_tr_top_up_3m',
        'created_at',
    )
    list_filter = ('session', 'channel', 'product', 'created_at')
    search_fields = ('session__user__username', 'channel', 'product')

    # Русификация полей
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"