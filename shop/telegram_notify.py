"""
Telegram orqali bildirishnoma yuborish.

Ishlashi uchun .env faylida quyidagilar to'ldirilgan bo'lishi kerak:
    TELEGRAM_BOT_TOKEN=...
    TELEGRAM_CHAT_ID=...

Agar bu ikkisi to'ldirilmagan bo'lsa, funksiya sukut bilan hech narsa
qilmaydi (sayt ishlashiga xalaqit bermaydi).

MUHIM (xato bo'lmasligi uchun): xabar 'parse_mode=HTML' bilan yuboriladi,
shuning uchun foydalanuvchi kiritgan har qanday matn (ism, izoh va h.k.)
Telegram'ga yuborishdan oldin html.escape() bilan tozalanadi. Aks holda
foydalanuvchi izohida "<", ">" yoki "&" belgisi bo'lsa, Telegram API
"can't parse entities" xatosi bilan xabarni butunlay rad etadi va
bildirishnoma hech qachon yetib bormaydi.
"""
import html
import logging

import requests
from decouple import config
from django.utils import timezone

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')


def send_telegram_message(text: str) -> bool:
    """Berilgan matnni Telegram bot orqali sizga yuboradi.

    Qaytaradi: True — muvaffaqiyatli yuborildi, False — yuborilmadi.
    Bu funksiya hech qachon exception ko'tarmaydi — Telegram ishlamay
    qolsa ham, chaqiruvchi kod (masalan, buyurtma saqlash) davom etishi
    kerak.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning(
            "Telegram xabari yuborilmadi: TELEGRAM_BOT_TOKEN yoki "
            "TELEGRAM_CHAT_ID .env faylida bo'sh. Iltimos, .env faylini "
            "tekshiring va serverni qayta ishga tushiring."
        )
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': text,
                'parse_mode': 'HTML',
            },
            timeout=10,
        )
        if response.ok:
            logger.info("Telegram xabari muvaffaqiyatli yuborildi (chat_id=%s).", TELEGRAM_CHAT_ID)
            return True

        logger.error(
            "Telegram xabar yuborilmadi. HTTP %s. Javob: %s",
            response.status_code, response.text,
        )
        return False
    except requests.Timeout:
        logger.error("Telegram API javob bermadi (timeout, 10s).")
        return False
    except requests.RequestException as exc:
        # Telegram ishlamay qolsa ham, mijoz buyurtma bera olishi kerak —
        # shuning uchun bu yerda xatolikni "yutib qo'yamiz", faqat log yozamiz.
        logger.error("Telegram xabar yuborishda xatolik: %s", exc)
        return False


def notify_wholesale_order(order) -> bool:
    """Yangi buyurtma haqida adminga Telegram orqali xabar yuboradi."""
    local_time = timezone.localtime(order.created_at) if order.created_at else timezone.localtime()
    text = (
        f"🛒 <b>YANGI BUYURTMA</b>\n\n"
        f"👤 Ism: {html.escape(order.name)}\n"
        f"📞 Telefon: {html.escape(order.phone)}\n"
        + (f"🏢 Korxona: {html.escape(order.company_name)}\n" if order.company_name else "")
        + f"📦 Mahsulot: {html.escape(str(order.product)) if order.product else '—'}\n"
        f"🔢 Miqdor: {order.quantity} dona\n"
        f"📝 Izoh: {html.escape(order.comment) if order.comment else '—'}\n"
        f"🆔 Buyurtma ID: #{order.pk}\n"
        f"🕐 Vaqt: {local_time.strftime('%Y-%m-%d %H:%M')}"
    )
    return send_telegram_message(text)


def notify_contact_message(msg) -> bool:
    text = (
        f"✉️ <b>Yangi xabar (Bog'lanish formasi)</b>\n\n"
        f"👤 Ism: {html.escape(msg.name)}\n"
        f"📞 Telefon: {html.escape(msg.phone) if msg.phone else '—'}\n"
        f"📧 Email: {html.escape(msg.email) if msg.email else '—'}\n"
        f"💬 Xabar: {html.escape(msg.message)}"
    )
    return send_telegram_message(text)
