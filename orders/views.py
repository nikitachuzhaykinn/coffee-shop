from django.shortcuts import render, redirect
from django.db import transaction
from cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from .utils import send_order_emails


def checkout(request):
    if not request.session.get('cart'):
        return redirect('cart:cart_detail')

    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.total_amount = cart.get_total_price()
                if request.user.is_authenticated:
                    order.user = request.user
                order.save()

                for item in cart:
                    modifier_data = [
                        {
                            'id': opt.id,
                            'name': opt.name,
                            'price_extra': str(opt.price_extra),
                        }
                        for opt in item['modifiers']
                    ]

                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['unit_price'],   # ← было item['price']
                        modifiers=modifier_data,
                    )

            cart.clear()
            send_order_emails(order)
            return redirect('orders:order_success', order_id=order.order_id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['first_name'] = request.user.first_name
            initial['last_name'] = request.user.last_name
            initial['email'] = request.user.email
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


def order_success(request, order_id):
    return render(request, 'orders/order_success.html', {'order_id': order_id})