from django.contrib import admin
from .models import Post, PostCategory

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)


admin.site.register(PostCategory)
