# SpongeFactory — Idish Yuvish Gubkasi Ishlab Chiqaruvchi Korxona Sayti

Django + PostgreSQL + Tailwind CSS asosida qurilgan, to'liq responsive va production darajasidagi korporativ/katalog sayt.

## 🧰 Texnologiyalar

- **Backend:** Django 5.0
- **Ma'lumotlar bazasi:** Lokal development uchun SQLite, production uchun PostgreSQL
- **Frontend:** HTML5, Tailwind CSS (CDN orqali), Vanilla JavaScript
- **Rasm bilan ishlash:** Pillow
- **Statik fayllar:** WhiteNoise (production uchun)

## 📁 Loyiha strukturasi

```
sponge_factory/
├── manage.py
├── requirements.txt
├── .env.example
├── sponge_factory/        # Loyiha sozlamalari (settings, urls, wsgi, asgi)
├── shop/                  # Asosiy ilova
│   ├── models.py          # Category, Product, ProductImage, Banner,
│   │                      # WholesaleOrder, ContactMessage, SiteSettings, AboutImage
│   ├── admin.py           # Admin panel + Dashboard
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── context_processors.py
├── templates/              # HTML shablonlar
│   ├── base.html
│   ├── 404.html / 500.html
│   ├── admin/custom_index.html   # Admin dashboard
│   └── shop/               # Sahifalar (home, product_list, product_detail,
│                            # about, contact, wholesale_order, order_success)
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/
└── media/                  # Yuklangan rasmlar (mahsulotlar, bannerlar va h.k.)
```

## 🚀 O'rnatish va ishga tushirish

### 1. Repozitoriyani oling va virtual muhit yarating

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 3. Muhit o'zgaruvchilarini sozlang

```bash
cp .env.example .env
```

`.env` faylini oching. Lokal ishlatishda standart sozlama SQLite bo'lib,
PostgreSQL serverini alohida yoqish shart emas:

```
SECRET_KEY=random-secret-key-generatsiya-qiling
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=sqlite
```

Lokal PostgreSQL ishlatmoqchi bo'lsangiz, `.env` ichida `DB_ENGINE=postgresql`
qiling va `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` qiymatlarini
to'ldiring. Railway yoki boshqa hostingda `DATABASE_URL` mavjud bo'lsa,
u avtomatik ishlatiladi.

> Agar oldingi versiyada `.env` fayli bo'lsa, undagi
> `DB_ENGINE=postgresql` qatorini `DB_ENGINE=sqlite` ga o'zgartiring.
> Yoki `.env` faylini o'chirib, `.env.example` dan yangisini yarating.

### 4. Migratsiyalarni bajaring

```bash
python manage.py migrate
```

SQLite ishlatilganda `db.sqlite3` fayli birinchi migratsiyada avtomatik yaratiladi.

### 5. Superuser (admin) yarating

```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushiring

```bash
python manage.py runserver
```

Windows PowerShell uchun to'liq buyruqlar:

```powershell
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Agar `.env` allaqachon mavjud bo'lsa, uni qayta yaratishdan oldin quyidagilarni
bajaring:

```powershell
(Get-Content .env) -replace 'DB_ENGINE=postgresql', 'DB_ENGINE=sqlite' | Set-Content .env
python manage.py migrate
python manage.py runserver
```

Sayt: **http://127.0.0.1:8000/**
Admin panel: **http://127.0.0.1:8000/admin/**

> Birinchi marta kirganda admin panelda **Sayt sozlamalari** bo'limiga o'tib, logo, telefon, email, Telegram, manzil va matnlarni to'ldiring — bu ma'lumotlar butun sayt bo'ylab (header, footer, bog'lanish sahifasi) avtomatik ko'rsatiladi. Keyin **Kategoriyalar** va **Mahsulotlar** qo'shing.

## ⚙️ Admin panelda boshqariladigan bo'limlar

| Bo'lim | Imkoniyat |
|---|---|
| **Dashboard** | Jami mahsulotlar, buyurtmalar, yangi buyurtmalar, kategoriyalar va o'qilmagan xabarlar statistikasi + so'nggi 5 ta buyurtma |
| **Mahsulotlar** | To'liq CRUD, rasm, narx, kategoriya, ombordagi soni, SEO maydonlari, galereya rasmlari (inline) |
| **Kategoriyalar** | Nomi, slug, tartib raqami, faollik holati |
| **Bannerlar** | Bosh sahifadagi slayder rasm/matnlari |
| **Optom buyurtmalar** | Foydalanuvchilar yuborgan buyurtmalar, holatini o'zgartirish (Yangi / Ko'rib chiqilmoqda / Bajarildi / Bekor qilindi) |
| **Kontakt xabarlari** | Bog'lanish formasidan kelgan xabarlar |
| **Sayt sozlamalari** | Logo, telefon, email, Telegram, manzil, Google xarita, matnlar (bitta yagona yozuv — singleton) |
| **Biz haqimizda rasmlari** | "Biz haqimizda" sahifasidagi galereya |

## 📱 Responsive dizayn

- Mobile-first yondashuv, Tailwind'ning `sm / md / lg / xl` breakpointlaridan foydalanilgan.
- Mahsulotlar: mobil — 1 ustun, planshet (`sm`) — 2 ustun, kompyuter (`lg`) — 3 ustun, katta ekran (`xl`) — 4 ustun.
- Header mobil/planshetda hamburger menyuga aylanadi (`lg` dan pastda).
- Barcha rasm/kontaynerlarda `overflow-x-hidden` va `max-w-full` qoidalariga rioya qilingan — gorizontal scroll chiqmaydi.

## 🔍 SEO

Har bir sahifa (`base.html`) `<title>` va `<meta name="description">` teglarini dinamik tarzda oladi:
- Mahsulot sahifasida — mahsulotning `meta_title` / `meta_description` maydonlaridan (bo'sh bo'lsa, avtomatik mahsulot nomi/tavsifidan).
- Boshqa sahifalarda — Sayt sozlamalaridagi umumiy meta ma'lumotlardan.

## 🖼️ Media va statik fayllar

- Development rejimida (`DEBUG=True`) media va static fayllar Django orqali avtomatik xizmat qiladi.
- Production uchun:
  ```bash
  python manage.py collectstatic
  ```
  va WhiteNoise orqali statik fayllar, alohida sozlangan media server (yoki S3/Cloud storage) orqali media fayllar xizmat qiladi.

## 🌐 Production uchun tavsiyalar

1. `.env` faylida `DEBUG=False` qiling va `ALLOWED_HOSTS` ga domeningizni kiriting.
2. `SECRET_KEY`ni yangi, tasodifiy qiymat bilan almashtiring.
3. `gunicorn sponge_factory.wsgi:application` orqali ishga tushiring (Nginx bilan birga).
4. Media fayllar uchun doimiy saqlash joyi (masalan, S3 yoki VPS diskida alohida volume) tayyorlang.
5. HTTPS sertifikat (Let's Encrypt) o'rnating.

## 🎨 Dizayn haqida eslatma

Loyihada Tailwind CSS **CDN** orqali ulangan — bu darhol ishlaydi va qo'shimcha build jarayoni talab qilmaydi. Agar siz to'liq production optimallashtirish (`purge`/`minify`, offline build) xohlasangiz, `django-tailwind` yoki Tailwind CLI + PostCSS pipeline'ni qo'shishingiz mumkin; barcha shablonlar shu narsaga tayyor holda toza semantik klasslar bilan yozilgan.

## 📄 Litsenziya

Ushbu loyiha buyurtma asosida ishlab chiqilgan namunaviy web sayt bo'lib, xohlagan tarzda moslashtirib ishlatishingiz mumkin.
