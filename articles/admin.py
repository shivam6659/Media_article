from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'publish_date')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'author__username', 'category')


# admin.site.register(Article)