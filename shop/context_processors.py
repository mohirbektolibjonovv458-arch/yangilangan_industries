from .models import SiteSettings, Category


def site_settings(request):
    """Sayt sozlamalari va kategoriyalarni barcha shablonlarda mavjud qiladi
    (header, footer, contact ma'lumotlari uchun)."""
    return {
        'site_settings': SiteSettings.load(),
        'nav_categories': Category.objects.filter(is_active=True).order_by('order', 'name'),
    }
