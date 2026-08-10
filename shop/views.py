from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, WholesaleOrderForm
from .models import AboutImage, Banner, Category, Product, SiteSettings
from .telegram_notify import notify_contact_message, notify_wholesale_order


def home(request):
    """Bosh sahifa: banner, kompaniya haqida qisqa ma'lumot, mashhur mahsulotlar."""
    settings_obj = SiteSettings.load()
    banners = Banner.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]

    if not featured_products:
        # Agar "mashhur" deb belgilangan mahsulot bo'lmasa, oxirgi qo'shilganlarni ko'rsatamiz
        featured_products = Product.objects.filter(is_active=True).select_related('category')[:8]

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'settings': settings_obj,
        'page_title': settings_obj.meta_title or f"{settings_obj.site_name} — Sifatli idish yuvish gubkalari",
        'page_description': settings_obj.meta_description or settings_obj.about_short,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Mahsulotlar ro'yxati: qidiruv va kategoriya bo'yicha filter, pagination."""
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query)
        )

    active_category = None
    if category_slug:
        active_category = categories.filter(slug=category_slug).first()
        if active_category:
            products = products.filter(category=active_category)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'active_category': active_category,
        'query': query,
        'page_title': "Mahsulotlar",
        'page_description': "Idish yuvish gubkalari katalogi — sifatli va arzon narxlarda.",
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    """Mahsulot tafsiloti sahifasi."""
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)
    gallery_images = product.images.all()
    related_products = Product.objects.filter(
        is_active=True, category=product.category
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'gallery_images': gallery_images,
        'related_products': related_products,
        'page_title': product.seo_title,
        'page_description': product.seo_description,
    }
    return render(request, 'shop/product_detail.html', context)


def about(request):
    """Biz haqimizda sahifasi."""
    settings_obj = SiteSettings.load()
    about_images = AboutImage.objects.all()
    context = {
        'settings': settings_obj,
        'about_images': about_images,
        'page_title': "Biz haqimizda",
        'page_description': settings_obj.about_short,
    }
    return render(request, 'shop/about.html', context)


def contact(request):
    """Bog'lanish sahifasi: kontakt ma'lumotlari, xarita va forma."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            notify_contact_message(contact_message)
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.")
            return redirect('shop:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': "Bog'lanish",
        'page_description': "Biz bilan bog'laning — telefon, telegram, email yoki forma orqali.",
    }
    return render(request, 'shop/contact.html', context)


def wholesale_order(request):
    """Optom buyurtma sahifasi va forma."""
    preselected_product = request.GET.get('product')
    preselected_qty = request.GET.get('qty')

    if request.method == 'POST':
        form = WholesaleOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            notify_wholesale_order(order)
            messages.success(
                request,
                "Buyurtmangiz qabul qilindi! Menejerlarimiz tez orada siz bilan bog'lanadi."
            )
            return redirect('shop:order_success')
    else:
        initial = {}
        if preselected_product:
            product_obj = Product.objects.filter(slug=preselected_product, is_active=True).first()
            if product_obj:
                initial['product'] = product_obj.pk
        if preselected_qty and preselected_qty.isdigit() and int(preselected_qty) > 0:
            initial['quantity'] = int(preselected_qty)
        form = WholesaleOrderForm(initial=initial)

    context = {
        'form': form,
        'page_title': "Optom buyurtma",
        'page_description': "Ishlab chiqaruvchidan to'g'ridan-to'g'ri optom narxlarda buyurtma bering.",
    }
    return render(request, 'shop/wholesale_order.html', context)


def order_success(request):
    context = {
        'page_title': "Buyurtma qabul qilindi",
        'page_description': "Buyurtmangiz muvaffaqiyatli yuborildi.",
    }
    return render(request, 'shop/order_success.html', context)


def custom_404(request, exception=None):
    context = {'page_title': "Sahifa topilmadi"}
    return render(request, '404.html', context, status=404)


def custom_500(request):
    context = {'page_title': "Server xatoligi"}
    return render(request, '500.html', context, status=500)
