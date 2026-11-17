from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Favorite, Order, Product


class ShopFlowTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Підгузки", slug="diapers", icon="👶")
        self.p = Product.objects.create(category=cat, name="Pampers 4", slug="pampers-4", price=Decimal("500"), old_price=Decimal("600"), stock=3)

    def test_pages_render(self):
        for url in [reverse("home"), reverse("catalog"), reverse("category", args=["diapers"]),
                    reverse("product", args=["pampers-4"]), reverse("cart"), reverse("login"), reverse("signup"),
                    reverse("catalog") + "?q=pamp&sort=cheap&sale=1"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_discount(self):
        self.assertEqual(self.p.discount, 17)

    def test_cart_and_checkout_reduces_stock(self):
        self.client.post(reverse("cart_add", args=[self.p.pk]), {"quantity": 5})  # capped to stock
        self.assertEqual(self.client.session["cart"], {str(self.p.pk): 3})
        r = self.client.post(reverse("checkout"), {
            "full_name": "Іван Петренко", "phone": "+380501234567", "delivery": "np",
            "city": "Київ", "address": "Відділення 1", "payment": "cod",
        })
        order = Order.objects.get()
        self.assertRedirects(r, reverse("order_done", args=[order.pk]))
        self.assertEqual(order.total, Decimal("1500"))
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock, 0)
        self.assertEqual(self.client.session["cart"], {})

    def test_checkout_requires_address_for_delivery(self):
        self.client.post(reverse("cart_add", args=[self.p.pk]))
        r = self.client.post(reverse("checkout"), {"full_name": "A", "phone": "+380501234567", "delivery": "np", "payment": "cod"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Order.objects.exists())

    def test_favorite_requires_login_then_toggles(self):
        r = self.client.post(reverse("toggle_favorite", args=[self.p.pk]))
        self.assertIn(reverse("login"), r.url)
        u = User.objects.create_user("u", password="pass12345!")
        self.client.force_login(u)
        self.client.post(reverse("toggle_favorite", args=[self.p.pk]))
        self.assertTrue(Favorite.objects.filter(user=u).exists())
        self.client.post(reverse("toggle_favorite", args=[self.p.pk]))
        self.assertFalse(Favorite.objects.exists())

    def test_signup_logs_in(self):
        r = self.client.post(reverse("signup"), {"username": "olena", "first_name": "Олена", "email": "o@example.com",
                                                 "password1": "Str0ngPass!x", "password2": "Str0ngPass!x"})
        self.assertRedirects(r, reverse("home"))
        self.assertEqual(self.client.get(reverse("account")).status_code, 200)

    def test_admin_pages_for_staff(self):
        self.client.force_login(User.objects.create_superuser("a", "a@x.com", "pass"))
        for name in ["admin:store_product_changelist", "admin:store_order_changelist", "admin:store_category_changelist"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
