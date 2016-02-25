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


def update_details(request):
    if request.method == 'POST':
        if request.is_ajax():
            which_service = int(request.POST.get('variant'))
            quantity = int(request.POST.get('quantity'))
            product = ProductVariant.objects.get(pk=which_service).product
            cart = Cart.for_session_cart(request.cart, discounts=request.discounts)
            product_variants = product.variants.all()
            # remove all variants form cart, if any. Avoids duplicate varians: weekly,
            # biweekly in one cart
            for line in cart:
                if line.product in product_variants:
                    cart.add(line.product, quantity=0, replace=True)

            variant = product.variants.get(id=which_service)
            cart.add(variant, quantity, replace=True)  # data?
            # import ipdb; ipdb.set_trace()
            for line in cart:
                data = None
                if line.product.pk == which_service:
                    data = request.POST
                    response = {
                        'productName': line.product.product.name,
                        'subtotal': currencyfmt(
                            line.get_total().gross,
                            line.get_total().currency),
                        'total': 0}
                    if cart:
                        response['total'] = currencyfmt(
                            cart.get_total().gross, cart.get_total().currency)
                    return JsonResponse(response)

        return HttpResponseRedirect(
                reverse('checkout:details', kwargs={'step': 'details'}))

    return redirect('checkout:index')
