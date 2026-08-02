from django.contrib import admin
from django.utils.safestring import mark_safe
from posts.models import Post


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'show_image', 'date', 'author')
    list_display_links = ('title',)
    fields = ('title', 'slug', 'show_image', 'date', 'author')
    readonly_fields = ('show_image','date')
    @admin.display(description='date')
    def date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @admin.display(description='image')
    def show_image(self, obj):

        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' alt='image' width='50'  />")
        return 'image_not_found!'