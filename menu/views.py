from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Product, Cart, CartItem, Promotion


# Главная страница
def index(request):
    return render(request, "menu/index.html")


# Страница меню с категориями
def menu(request):
    categories = Category.objects.prefetch_related("products").all()
    return render(request, "menu/menu.html", {"categories": categories})


# Вспомогательная функция для получения или создания корзины
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        else:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    return cart


# Страница корзины
def cart(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(
        request,
        "menu/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


# Добавление товара в корзину
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")


# Удаление товара из корзины
def remove_from_cart(request, product_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


# Оформление заказа
@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == "POST":
        # Логика оформления заказа
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        # Очистка корзины после оформления заказа
        cart_items.delete()
        return render(
            request, "menu/checkout_success.html", {"phone": phone, "email": email}
        )

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(
        request,
        "menu/checkout.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


# Страницы отдельных категорий меню
def menu_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    return render(
        request, "menu/category.html", {"category": category, "products": products}
    )


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    return render(
        request, "menu/category.html", {"category": category, "products": products}
    )


def slider(request):
    promotions = Promotion.objects.filter(active=True)
    return render(request, "index.html", {"promotions": promotions})


def test_session(request):
    # Сохраняем тестовые данные в сессии
    request.session["test_key"] = "test_value"
    return JsonResponse({"message": "Data added to session"})


def get_session(request):
    value = request.session.get("test_key", "No data found")
    return JsonResponse({"test_key": value})


def clear_session(request):
    request.session.flush()
    return JsonResponse({"message": "Session cleared"})
