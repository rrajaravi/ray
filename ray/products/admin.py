from django.contrib import admin

from .models import Product, ProductType
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'name', 'url')
    search_fields = ('url',)
    readonly_fields = ('name', 'product_id')


class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Product, ProductsAdmin)
admin.site.register(ProductType, ProductTypesAdmin)
