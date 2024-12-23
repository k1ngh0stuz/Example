from django.contrib import admin
from .models import Article, Category
from django.utils.safestring import mark_safe


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    # Что показывать в админке
    list_display = ('pk', 'title', 'category', 'created_at', 'updated_at', 'get_photo', 'is_publisher')
    list_display_links = ('pk', 'title')
    list_editable = ('is_publisher',)


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src ="{obj.photo.url}" width="50">')

    get_photo.short_description = 'Миниатюра'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
