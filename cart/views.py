from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from catalog.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_clear(request):
    request.session.flush()
    return redirect('cart:cart_detail')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    modifier_options = request.POST.getlist('modifier_options')
    
    cart.add(product=product, quantity=quantity, modifier_options=modifier_options)
    
    # Возвращаем счетчик + уведомление
    response = render(request, 'cart/_cart_count.html', {'cart': cart})
    response['HX-Trigger'] = 'cart-added'
    return response


@require_POST
def cart_remove(request, product_key):
    cart = Cart(request)
    cart.remove(product_key)
    
    html = render_to_string('cart/_cart_main_container.html', {'cart': cart}, request)
    html += render_to_string('cart/_cart_count.html', {'cart': cart}, request)
    return HttpResponse(html)

@require_POST
def cart_update(request, product_key):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart.remove(product_key)
    else:
        cart.update_quantity(product_key, quantity)
    
    html = render_to_string('cart/_cart_main_container.html', {'cart': cart}, request)
    html += render_to_string('cart/_cart_count.html', {'cart': cart}, request)
    return HttpResponse(html)