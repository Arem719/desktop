from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CheckoutForm, SignUpForm
from .models import Category, Favorite, Order, OrderItem, Product

SORTS = {
    "popular": ("-is_hit", "name"),
    "cheap": ("price",),
    "expensive": ("-price",),
    "new": ("-created",),
}


def _filtered(request, qs):
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if request.GET.get("sale"):
        qs = qs.filter(old_price__gt=F("price"))
    if request.GET.get("instock"):
        qs = qs.filter(stock__gt=0)
    sort = request.GET.get("sort", "popular")
    return qs.order_by(*SORTS.get(sort, SORTS["popular"])), q, sort


def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/home.html", {
        "hits": products.filter(is_hit=True)[:8],
        "sale": products.filter(old_price__gt=F("price"))[:8],
    })


def catalog(request, slug=None):
    category = get_object_or_404(Category, slug=slug) if slug else None
    qs = Product.objects.filter(is_active=True).select_related("category")
    if category:
        qs = qs.filter(category=category)
    qs, q, sort = _filtered(request, qs)
    page = Paginator(qs, 12).get_page(request.GET.get("page"))
    return render(request, "store/catalog.html", {"category": category, "page": page, "q": q, "sort": sort})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, "store/product.html", {"product": product, "related": related})


# ---------- cart ----------

def cart_detail(request):
    cart = Cart(request)
    items = list(cart)
    return render(request, "store/cart.html", {"items": items, "total": sum((i["subtotal"] for i in items), 0)})


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if not product.in_stock:
        messages.error(request, "Товару немає в наявності")
    else:
        Cart(request).add(product, int(request.POST.get("quantity", 1)))
        messages.success(request, f"«{product.name}» додано в кошик")
    return redirect(request.POST.get("next") or "cart")


@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart(request).set(product, request.POST.get("quantity", 0))
    return redirect("cart")


@require_POST
def cart_remove(request, pk):
    Cart(request).remove(get_object_or_404(Product, pk=pk))
    return redirect("cart")


def checkout(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        return redirect("cart")
    initial = {}
    if request.user.is_authenticated:
        u = request.user
        initial = {"full_name": u.get_full_name() or u.first_name, "email": u.email}
        last = u.orders.first()
        if last:
            initial.update(phone=last.phone, city=last.city, address=last.address, delivery=last.delivery)
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            total = 0
            for i in items:
                # lock row and re-check stock so two buyers can't oversell
                p = Product.objects.select_for_update().get(pk=i["product"].pk)
                qty = min(i["quantity"], p.stock)
                if qty == 0:
                    continue
                OrderItem.objects.create(order=order, product=p, name=p.name, price=p.price, quantity=qty)
                p.stock -= qty
                p.save(update_fields=["stock"])
                total += p.price * qty
            if total == 0:
                transaction.set_rollback(True)
                messages.error(request, "На жаль, товари з кошика закінчились")
                return redirect("cart")
            order.total = total
            order.save(update_fields=["total"])
        cart.clear()
        return redirect("order_done", pk=order.pk)
    return render(request, "store/checkout.html", {"form": form, "cart": cart, "items": items})


def order_done(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user_id and order.user != request.user:
        return redirect("home")
    return render(request, "store/order_done.html", {"order": order})


# ---------- favorites ----------

@require_POST
def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_authenticated:
        messages.info(request, "Увійдіть, щоб додавати товари в обране")
        return redirect_to_login(request.POST.get("next") or product.get_absolute_url())
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
    return redirect(request.POST.get("next") or product.get_absolute_url())


@login_required
def favorites(request):
    products = Product.objects.filter(liked_by__user=request.user, is_active=True)
    return render(request, "store/favorites.html", {"products": products})


# ---------- account ----------

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Вітаємо! Акаунт створено")
        return redirect("home")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def account(request):
    return render(request, "store/account.html", {"orders": request.user.orders.prefetch_related("items")})
