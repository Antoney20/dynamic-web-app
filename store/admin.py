from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from store.models import Product, SiteConfig, Testimonial, Transaction,Banner
from blog.models import Post

admin.site.register(Post)

admin.site.register(Banner)


@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "discount",
        "inventory_count",
        "active",
    )

    # Display preview of image in admin
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 200px"/>'.format(obj.image.url))

    image_tag.short_description = "Product Image Preview"
    readonly_fields = ["image_tag"]

    # Formatted discount display for admin list
    def discount(self, obj):
        return f"{obj.discount_percent}%"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("datetime", "product_id")
    
    
admin.site.register(Testimonial)