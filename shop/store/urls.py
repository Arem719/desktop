from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("catalog/<slug:slug>/", views.catalog, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:pk>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/", views.order_done, name="order_done"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/toggle/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("signup/", views.signup, name="signup"),
    path("account/", views.account, name="account"),
]
