from django.http.response import Http404
from django.shortcuts import redirect, get_object_or_404

from .core import Checkout
from ..cart import Cart
from ..cart.utils import contains_unavailable_products

from saleor.product.models import Product, ProductVariant, Category


def details(request, step):

    if not request.cart:
        # TODO: get the product id from request url parameters
        product_id = 2
        products = Product.objects.get_available_products().select_subclasses()
        products = products.prefetch_related('variants__stock')
        product = get_object_or_404(products, id=product_id)
        product_slug = 'flyttstadning'
        product_variant = product.variants.first()
        if product.get_slug() != product_slug:
            raise ValueError('Slug not equals')
        # import ipdb; ipdb.set_trace()
        cart = Cart.for_session_cart(request.cart, discounts=request.discounts)
        cart.add(product_variant, 1)
    if not request.cart or contains_unavailable_products(
            Cart.for_session_cart(request.cart, discounts=request.discounts)):
        return redirect('cart:index')
    checkout = Checkout(request)
    if not step:
        return redirect(checkout.get_next_step())
    try:
        step = checkout[step]
    except KeyError:
        raise Http404()
    if step not in checkout.available_steps():
        return redirect(checkout.get_next_step())
    response = step.process(
        extra_context={'checkout': checkout})
    if not response:
        checkout.save()
        return redirect(checkout.get_next_step())
    return response
