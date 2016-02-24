from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse

from .core import Checkout
from ..cart import Cart
from ..cart.utils import contains_unavailable_products
from ..cart.forms import ReplaceCartLineForm
from .forms import get_form_class_for_service

from babeldjango.templatetags.babel import currencyfmt

from saleor.product.models import Product, ProductVariant, Category


def details(request, step, product_id=None):

    if not request.cart:
        step = 'details'

    checkout = Checkout(request)
    # import ipdb; ipdb.set_trace()
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


def update_details(request, which_service):
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':

        product = Product.objects.get(pk=which_service)
        service_form_class = get_form_class_for_service(product)
        service_form = service_form_class(cart=request.cart,
                product=product,data=request.POST or None)

        variant_id = int(service_form.data['variant'])
        quantity = int(service_form.data['quantity'])
        cart = Cart.for_session_cart(request.cart, discounts=request.discounts)
        product_variants = product.variants.all()
        # remove all variants form cart, if any. Avoids duplicate varians: weekly,
        # biweekly in one cart
        for line in cart:
            if line.product in product_variants:
                cart.add(line.product, quantity=0, replace=True)

        # import ipdb; ipdb.set_trace()
        variant = product.variants.get(id=variant_id)
        cart.add(variant, quantity, replace=True)  # data?

        return HttpResponseRedirect(
                reverse('checkout:details', kwargs={'step': 'details'}))

    return redirect('checkout:index')
