from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Favorite, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order", "product_count")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Товарів")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price", "old_price", "stock", "is_hit", "is_active")
    list_display_links = ("thumb", "name")
    list_editable = ("price", "stock", "is_hit", "is_active")
    list_filter = ("category", "is_active", "is_hit", "brand")
    search_fields = ("name", "brand", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 30
    actions = ("hide", "show")

    @admin.display(description="")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:6px">', obj.image.url)
        return "—"

    @admin.action(description="Сховати вибрані")
    def hide(self, request, qs):
        qs.update(is_active=False)

    @admin.action(description="Показати вибрані")
    def show(self, request, qs):
        qs.update(is_active=True)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "full_name", "phone", "total", "delivery", "status")
    list_editable = ("status",)
    list_filter = ("status", "delivery", "payment", "created")
    search_fields = ("id", "full_name", "phone", "email")
    readonly_fields = ("total", "created", "user")
    inlines = (OrderItemInline,)
    date_hierarchy = "created"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created")
