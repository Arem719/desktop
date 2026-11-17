from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Product

CATS = [
    ("Побутова хімія", "household", "🧴"),
    ("Прання", "laundry", "🧺"),
    ("Підгузки", "diapers", "👶"),
    ("Гігієна", "hygiene", "🧼"),
]

# (category, name, brand, volume, price, old_price, stock, hit)
PRODUCTS = [
    ("household", "Засіб для миття посуду Лимон", "Fairy", "900 мл", 89, 109, 40, True),
    ("household", "Засіб для чищення ванної", "Cillit Bang", "750 мл", 149, None, 25, False),
    ("household", "Гель для унітазу Морська свіжість", "Domestos", "1 л", 95, 119, 30, True),
    ("household", "Засіб для миття скла", "Mr Muscle", "500 мл", 79, None, 18, False),
    ("household", "Таблетки для посудомийки All in 1", "Finish", "60 шт", 499, 589, 12, True),
    ("household", "Засіб для підлоги", "Mr Proper", "1 л", 99, None, 0, False),
    ("laundry", "Пральний порошок Автомат Color", "Persil", "4.5 кг", 389, 449, 20, True),
    ("laundry", "Гель для прання Universal", "Ariel", "1.95 л", 329, None, 15, False),
    ("laundry", "Капсули для прання 3в1", "Tide", "45 шт", 459, 529, 10, True),
    ("laundry", "Ополіскувач для білизни", "Lenor", "1.8 л", 189, None, 22, False),
    ("laundry", "Плямовивідник Oxi Action", "Vanish", "1 л", 219, 259, 14, False),
    ("diapers", "Підгузки Active Baby 4 (9–14 кг)", "Pampers", "76 шт", 799, 899, 16, True),
    ("diapers", "Підгузки-трусики 5 (12–17 кг)", "Huggies", "48 шт", 649, None, 12, True),
    ("diapers", "Підгузки Premium Care 2 (4–8 кг)", "Pampers", "68 шт", 729, None, 9, False),
    ("diapers", "Підгузки Ultra Comfort 3 (5–9 кг)", "Huggies", "78 шт", 589, 659, 0, False),
    ("diapers", "Вологі серветки дитячі Sensitive", "Pampers", "4×52 шт", 199, 239, 35, True),
    ("hygiene", "Рідке мило Алое Віра", "Palmolive", "500 мл", 69, None, 50, False),
    ("hygiene", "Зубна паста Total", "Colgate", "100 мл", 89, 99, 40, False),
    ("hygiene", "Туалетний папір 3-шаровий", "Zewa", "8 рулонів", 149, 175, 30, True),
    ("hygiene", "Шампунь Проти лупи", "Head & Shoulders", "400 мл", 179, None, 20, False),
    ("hygiene", "Гель для душу Чоловічий", "Nivea Men", "500 мл", 129, 149, 26, False),
    ("hygiene", "Ватні диски", "Bella", "120 шт", 45, None, 60, False),
]


UA = dict(zip("абвгґдеєжзиіїйклмнопрстуфхцчшщьюяʼ'",
              ["a","b","v","h","g","d","e","ie","zh","z","y","i","i","i","k","l","m","n","o","p","r","s","t","u","f","kh","ts","ch","sh","shch","","iu","ia","",""]))


def translit(text):
    return "".join(UA.get(c, c) for c in text.lower())


class Command(BaseCommand):
    help = "Fill the shop with demo categories, products and an admin user (admin / admin12345)."

    def handle(self, *args, **opts):
        cats = {}
        for i, (name, slug, icon) in enumerate(CATS):
            cats[slug], _ = Category.objects.update_or_create(slug=slug, defaults={"name": name, "icon": icon, "order": i})
        for cat, name, brand, vol, price, old, stock, hit in PRODUCTS:
            slug = slugify(translit(f"{brand}-{name}-{vol}"))[:200]
            Product.objects.update_or_create(slug=slug, defaults=dict(
                category=cats[cat], name=name, brand=brand, volume=vol, price=Decimal(price),
                old_price=Decimal(old) if old else None, stock=stock, is_hit=hit,
                description=f"{brand} — {name.lower()}. Обʼєм/кількість: {vol}. Оригінальна продукція.",
            ))
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin12345")
            self.stdout.write("Admin created: admin / admin12345 — change the password!")
        self.stdout.write(self.style.SUCCESS(f"{Product.objects.count()} products ready"))
