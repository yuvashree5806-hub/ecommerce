import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from products.models import Category, Product


def index(request):
    return render(request, 'index.html')


def products_page(request):
    return render(request, 'products.html')


def cart_page(request):
    return render(request, 'cart.html')


def checkout_page(request):
    return render(request, 'checkout.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def order_success_page(request):
    return render(request, 'order-success.html')


def orders_page(request):
    return render(request, 'orders.html')


def product_details_page(request):
    return render(request, 'product-details.html')


def get_guest_user():
    user, _ = User.objects.get_or_create(
        username='guest',
        defaults={'email': 'guest@example.com'}
    )
    return user


def api_products(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.select_related('category').all()
    if query:
        products = products.filter(name__icontains=query)

    result = []
    for product in products:
        image_url = '/static/images/laptop.jpg'
        if product.image and hasattr(product.image, 'url'):
            image_url = product.image.url
        result.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category.name if product.category else None,
            'stock': product.stock,
            'image': image_url,
        })

    return JsonResponse({'products': result})


def api_cart_list(request):
    user = get_guest_user()
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return JsonResponse({'items': [], 'total': '0.00'})

    items = []
    total = 0
    for item in cart.items.select_related('product').all():
        line_total = item.quantity * item.product.price
        total += line_total
        image_url = '/static/images/laptop.jpg'
        if item.product.image and hasattr(item.product.image, 'url'):
            image_url = item.product.image.url
        items.append({
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity,
            'line_total': str(line_total),
            'image': image_url,
        })

    return JsonResponse({'items': items, 'total': str(total)})


@csrf_exempt
def api_cart_add(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    product_id = payload.get('product_id')
    if not product_id:
        return HttpResponseBadRequest('Missing product_id')

    product = get_object_or_404(Product, pk=product_id)
    user = get_guest_user()
    cart, _ = Cart.objects.get_or_create(user=user)
    quantity = int(payload.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': max(1, quantity)})
    if not created:
        item.quantity += quantity
        if item.quantity <= 0:
            item.delete()
            return JsonResponse({'success': True, 'deleted': True})
        item.save()

    return JsonResponse({'success': True, 'item_id': item.id})


@csrf_exempt
def api_cart_remove(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON payload')

    item_id = payload.get('item_id')
    if not item_id:
        return HttpResponseBadRequest('Missing item_id')

    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    return JsonResponse({'success': True})


@csrf_exempt
def api_checkout(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    user = get_guest_user()
    cart = Cart.objects.filter(user=user).first()
    if not cart or not cart.items.exists():
        return JsonResponse({'success': False, 'message': 'Cart is empty'})

    total_amount = 0
    for item in cart.items.select_related('product').all():
        total_amount += item.product.price * item.quantity

    order = Order.objects.create(user=user, total_amount=total_amount)
    order_items = []
    for item in cart.items.select_related('product').all():
        order_items.append(OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price))
    OrderItem.objects.bulk_create(order_items)
    cart.items.all().delete()

    return JsonResponse({'success': True, 'order_id': order.id})


def api_product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    image_url = '/static/images/laptop.jpg'
    if product.image and hasattr(product.image, 'url'):
        image_url = product.image.url
    
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'category': product.category.name if product.category else None,
        'stock': product.stock,
        'image': image_url,
    })


def api_orders_list(request):
    user = get_guest_user()
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    result = []
    for order in orders:
        items = []
        for item in order.orderitem_set.select_related('product').all():
            image_url = '/static/images/laptop.jpg'
            if item.product.image and hasattr(item.product.image, 'url'):
                image_url = item.product.image.url
            items.append({
                'product_id': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price),
                'line_total': str(item.quantity * item.price),
                'image': image_url,
            })
        result.append({
            'id': order.id,
            'status': order.status,
            'total_amount': str(order.total_amount),
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': items
        })
    return JsonResponse({'orders': result})

