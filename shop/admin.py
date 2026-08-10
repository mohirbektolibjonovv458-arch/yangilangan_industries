from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    AboutImage, Banner, Category, ContactMessage, Product,
    ProductImage, SiteSettings, WholesaleOrder,
)


# ------------------------------------------------------------------
# Custom Admin Site — Dashboard bilan
# ------------------------------------------------------------------
class SpongeFactoryAdminSite(AdminSite):
    site_header = "SpongeFactory — Boshqaruv paneli"
    site_title = "SpongeFactory Admin"
    index_title = "Dashboard"
    index_template = 'admin/custom_index.html'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_products'] = Product.objects.count()
        extra_context['total_orders'] = WholesaleOrder.objects.count()
        extra_context['new_orders'] = WholesaleOrder.objects.filter(status='new').count()
        extra_context['total_categories'] = Category.objects.count()
        extra_context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        extra_context['recent_orders'] = WholesaleOrder.objects.select_related('product').order_by('-created_at')[:5]
        return super().index(request, extra_context)


admin_site = SpongeFactoryAdminSite(name='spongefactory_admin')


# ------------------------------------------------------------------
# Inlines
# ------------------------------------------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'order')


# ------------------------------------------------------------------
# Category
# ------------------------------------------------------------------
@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'product_count')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    @admin.display(description="Mahsulotlar soni")
    def product_count(self, obj):
        return obj.products.count()


# ------------------------------------------------------------------
# Product
# ------------------------------------------------------------------
@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'name', 'category', 'price', 'stock', 'is_featured', 'is_active', 'created_at')
    list_editable = ('is_featured',)
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_per_page = 25
    fieldsets = (
        ("Asosiy ma'lumot", {
            'fields': ('name', 'slug', 'category', 'price', 'stock', 'main_image')
        }),
        ("Tavsif", {
            'fields': ('short_description', 'description')
        }),
        ("Holat", {
            'fields': ('is_active', 'is_featured')
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:6px;" />', obj.main_image.url)
        return "—"


# ------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------
@admin.register(Banner, site=admin_site)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:70px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "—"


# ------------------------------------------------------------------
# WholesaleOrder
# ------------------------------------------------------------------
@admin.register(WholesaleOrder, site=admin_site)
class WholesaleOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'company_name', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'phone', 'company_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


# ------------------------------------------------------------------
# ContactMessage
# ------------------------------------------------------------------
@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)


# ------------------------------------------------------------------
# AboutImage
# ------------------------------------------------------------------
@admin.register(AboutImage, site=admin_site)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'caption', 'order')
    list_editable = ('order',)

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:70px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "—"


# ------------------------------------------------------------------
# SiteSettings (singleton)
# ------------------------------------------------------------------
@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Umumiy", {
            'fields': ('site_name', 'logo')
        }),
        ("Aloqa ma'lumotlari", {
            'fields': ('phone', 'phone_secondary', 'email', 'telegram', 'instagram', 'address', )
        }),
        ("Matnlar", {
            'fields': ('about_short', 'about_text', 'production_process', 'why_choose_us')
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description')
        }),
        ("Footer", {
            'fields': ('footer_copyright',)
        }),
    )

    def has_add_permission(self, request):
        # Faqat bitta yozuv bo'lishi kerak (singleton)
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # To'g'ridan-to'g'ri yagona obyektni tahrirlash sahifasiga yo'naltirish
        obj = SiteSettings.load()
        from django.shortcuts import redirect
        return redirect(reverse('admin:shop_sitesettings_change', args=[obj.pk]))
