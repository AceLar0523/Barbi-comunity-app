from django.contrib import admin
from .models import Barbie, BarbieImage

class BarbieImageInline(admin.TabularInline):
    model = BarbieImage
    extra = 1

@admin.register(Barbie)
class BarbieAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'release_year', 'barbie_type', 'in_box', 'is_favorite')
    list_filter = ('is_favorite', 'in_box', 'collection', 'release_year', 'manufacturer', 'barbie_type')
    search_fields = ('name', 'description', 'collection')
    inlines = [BarbieImageInline]

admin.site.register(BarbieImage)
