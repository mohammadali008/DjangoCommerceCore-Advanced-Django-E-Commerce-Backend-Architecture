from django.contrib import admin
from .models import *

# - Define ProductImage as line  -#
class ProductImageLine(admin.TabularInline):
    model = ProductImage

#Define ProductAttributeAdmin
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    exec  = 1

### Define AdminClass
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_type','upc','title','category','brand','soft_delete']
    list_filter = ['soft_delete']
    list_editable = ['soft_delete']
    search_fields = ['upc','title','category__name']
    inlines = [ProductImageLine]

#Define ProductTypeAdmin
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    inline = [ProductAttributeInline]


# Register your models here.
admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductType)
admin.site.register(ProductAttribute)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductAttributeValue)

















