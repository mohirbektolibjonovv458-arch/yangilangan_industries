from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

phone_validator = RegexValidator(
    regex=r'^\+?[0-9\s\-\(\)]{7,20}$',
    message="Telefon raqamini to'g'ri formatda kiriting. Masalan: +998901234567"
)


class Category(models.Model):
    """Mahsulot kategoriyasi (masalan: Oshxona gubkalari, Metall gubkalar)."""
    name = models.CharField("Nomi", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=120, unique=True, blank=True)
    description = models.TextField("Tavsif", blank=True)
    order = models.PositiveIntegerField("Tartib raqami", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_list') + f'?category={self.slug}'


class Product(models.Model):
    """Ishlab chiqarilayotgan gubka mahsuloti."""
    category = models.ForeignKey(
        Category, verbose_name="Kategoriya", on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    name = models.CharField("Nomi", max_length=150)
    slug = models.SlugField("Slug", max_length=180, unique=True, blank=True)
    price = models.DecimalField("Narxi (so'm)", max_digits=12, decimal_places=2)
    short_description = models.CharField("Qisqa tavsif", max_length=255)
    description = models.TextField("To'liq tavsif", blank=True)
    main_image = models.ImageField("Asosiy rasm", upload_to='products/')
    is_featured = models.BooleanField("Mashhur mahsulot", default=False,
                                       help_text="Bosh sahifada ko'rsatiladi")
    is_active = models.BooleanField("Faol (saytda ko'rinadi)", default=True)
    stock = models.PositiveIntegerField("Ombordagi soni (dona/quti)", default=0)

    # SEO
    meta_title = models.CharField("Meta title (SEO)", max_length=200, blank=True)
    meta_description = models.CharField("Meta description (SEO)", max_length=300, blank=True)

    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan sana", auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=False) or "mahsulot"
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    @property
    def seo_title(self):
        return self.meta_title or self.name

    @property
    def seo_description(self):
        return self.meta_description or self.short_description


class ProductImage(models.Model):
    """Mahsulotning qo'shimcha (galereya) rasmlari."""
    product = models.ForeignKey(Product, verbose_name="Mahsulot",
                                 on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("Rasm", upload_to='products/gallery/')
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.product.name} - rasm {self.order}"


class Banner(models.Model):
    """Bosh sahifadagi katta banner (slayder)."""
    title = models.CharField("Sarlavha", max_length=200)
    subtitle = models.CharField("Ost sarlavha", max_length=300, blank=True)
    image = models.ImageField("Rasm", upload_to='banners/')
    button_text = models.CharField("Tugma matni", max_length=50, default="Mahsulotlarni ko'rish")
    button_link = models.CharField("Tugma havolasi", max_length=200, default="/products/")
    order = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class WholesaleOrder(models.Model):
    """Optom buyurtma so'rovi."""

    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Ko\'rib chiqilmoqda'),
        ('done', 'Bajarildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    name = models.CharField("Ism familya", max_length=150)
    phone = models.CharField("Telefon", max_length=20, validators=[phone_validator])
    company_name = models.CharField("Korxona nomi", max_length=200, blank=True)
    product = models.ForeignKey(Product, verbose_name="Mahsulot",
                                 on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='wholesale_orders')
    quantity = models.PositiveIntegerField("Miqdor")
    comment = models.TextField("Izoh", blank=True)
    status = models.CharField("Holati", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Yuborilgan vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "Optom buyurtma"
        verbose_name_plural = "Optom buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.product} ({self.quantity} dona)"


class ContactMessage(models.Model):
    """Bog'lanish sahifasidagi kontakt forma xabarlari."""
    name = models.CharField("Ism", max_length=150)
    phone = models.CharField("Telefon", max_length=20, validators=[phone_validator], blank=True)
    email = models.EmailField("Email", blank=True)
    message = models.TextField("Xabar")
    created_at = models.DateTimeField("Yuborilgan vaqti", auto_now_add=True)
    is_read = models.BooleanField("O'qilgan", default=False)

    class Meta:
        verbose_name = "Kontakt xabari"
        verbose_name_plural = "Kontakt xabarlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"


class SiteSettings(models.Model):
    """Sayt bo'yicha umumiy sozlamalar (singleton — faqat bitta yozuv bo'ladi)."""
    site_name = models.CharField("Sayt nomi", max_length=100, default="SpongeFactory")
    logo = models.ImageField("Logo", upload_to='site/', blank=True, null=True)

    phone = models.CharField("Telefon", max_length=20, blank=True)
    phone_secondary = models.CharField("Qo'shimcha telefon", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram (havola yoki @username)", max_length=150, blank=True)
    instagram = models.CharField("Instagram (havola)", max_length=150, blank=True)
    address = models.CharField("Manzil", max_length=255, blank=True)
    google_map_embed = models.TextField(
        "Google Map iframe kodi", blank=True,
        help_text="Google Maps dan 'Share > Embed a map' orqali olingan <iframe> kodini shu yerga joylashtiring."
    )

    about_short = models.TextField("Bosh sahifadagi qisqa ma'lumot", blank=True)
    about_text = models.TextField("Biz haqimizda — to'liq matn", blank=True)
    production_process = models.TextField("Ishlab chiqarish jarayoni matni", blank=True)
    why_choose_us = models.TextField("Nima uchun bizni tanlashadi", blank=True)

    meta_title = models.CharField("Sayt uchun umumiy meta title", max_length=200, blank=True)
    meta_description = models.CharField("Sayt uchun umumiy meta description", max_length=300, blank=True)

    footer_copyright = models.CharField(
        "Footer copyright matni", max_length=200,
        default="© 2026 SpongeFactory. Barcha huquqlar himoyalangan."
    )

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        self.pk = 1  # Har doim faqat bitta yozuv (singleton)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # O'chirishga ruxsat berilmaydi

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutImage(models.Model):
    """Biz haqimizda sahifasidagi galereya rasmlari (ishlab chiqarish jarayoni)."""
    image = models.ImageField("Rasm", upload_to='about/')
    caption = models.CharField("Tavsif (ixtiyoriy)", max_length=200, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Biz haqimizda rasm"
        verbose_name_plural = "Biz haqimizda rasmlari"
        ordering = ['order', 'id']

    def __str__(self):
        return self.caption or f"Rasm #{self.pk}"
