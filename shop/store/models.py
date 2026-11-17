from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Назва", max_length=100)
    slug = models.SlugField("URL", unique=True)
    icon = models.CharField("Іконка (емодзі)", max_length=8, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категорія")
    name = models.CharField("Назва", max_length=200)
    slug = models.SlugField("URL", unique=True, max_length=220)
    brand = models.CharField("Бренд", max_length=100, blank=True)
    description = models.TextField("Опис", blank=True)
    volume = models.CharField("Обʼєм / кількість", max_length=50, blank=True, help_text="Напр. 1 л, 52 шт")
    price = models.DecimalField("Ціна, грн", max_digits=10, decimal_places=2)
    old_price = models.DecimalField("Стара ціна, грн", max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField("Залишок", default=0)
    image = models.ImageField("Фото", upload_to="products/", blank=True)
    is_active = models.BooleanField("Показувати", default=True)
    is_hit = models.BooleanField("Хіт продажів", default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_hit", "name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", args=[self.slug])

    @property
    def discount(self):
        if self.old_price and self.old_price > self.price:
            return int(round((1 - self.price / self.old_price) * 100))
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="liked_by")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Обране"
        verbose_name_plural = "Обране"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Нове"
        CONFIRMED = "confirmed", "Підтверджене"
        SHIPPED = "shipped", "Відправлене"
        DONE = "done", "Виконане"
        CANCELED = "canceled", "Скасоване"

    class Delivery(models.TextChoices):
        NOVA_POSHTA = "np", "Нова Пошта"
        UKRPOSHTA = "up", "Укрпошта"
        PICKUP = "pickup", "Самовивіз"

    class Payment(models.TextChoices):
        COD = "cod", "Оплата при отриманні"
        CARD = "card", "Переказ на картку"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Користувач")
    full_name = models.CharField("ПІБ", max_length=150)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email", blank=True)
    delivery = models.CharField("Доставка", max_length=10, choices=Delivery.choices, default=Delivery.NOVA_POSHTA)
    city = models.CharField("Місто", max_length=100, blank=True)
    address = models.CharField("Відділення / адреса", max_length=200, blank=True)
    payment = models.CharField("Оплата", max_length=10, choices=Payment.choices, default=Payment.COD)
    comment = models.TextField("Коментар", blank=True)
    status = models.CharField("Статус", max_length=12, choices=Status.choices, default=Status.NEW)
    total = models.DecimalField("Сума, грн", max_digits=10, decimal_places=2, default=Decimal("0"))
    created = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення №{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Товар")
    name = models.CharField("Назва", max_length=200)
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("К-сть")

    class Meta:
        verbose_name = "Позиція"
        verbose_name_plural = "Позиції"

    @property
    def subtotal(self):
        return self.price * self.quantity
