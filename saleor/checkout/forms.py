from django import forms
from django.utils.translation import ugettext_lazy as _

from ..cart.forms import AddToCartForm

class AddressChoiceIterator(forms.models.ModelChoiceIterator):

    def __iter__(self):
        if self.field.copy_choice:
            yield self.field.copy_choice_value, self.field.copy_choice_label
        for obj in self.queryset:
            yield self.choice(obj)
        yield self.field.new_choice_value, self.field.new_choice_label


class AddressChoiceField(forms.ModelChoiceField):
    copy_choice_value = 'copy'
    copy_choice_label = _('Use shipping address for billing')
    new_choice_value = 'new'
    new_choice_label = _('Enter a new address')

    def __init__(self, queryset, can_copy, *args, **kwargs):
        if queryset or can_copy:
            widget = forms.RadioSelect
        else:
            widget = forms.HiddenInput
        if not can_copy:
            self.copy_choice_value = None
        super(AddressChoiceField, self).__init__(
            widget=widget, queryset=queryset, *args, **kwargs)
        self.widget.field_instance = self

    def validate(self, value):
        if not self.is_special_choice(value):
            return super(AddressChoiceField, self).validate(value)

    def to_python(self, value):
        if self.is_special_choice(value):
            return value
        else:
            return super(AddressChoiceField, self).to_python(value)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return AddressChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

    def is_special_choice(self, value):
        return value in (self.new_choice_value, self.copy_choice_value)


class UserAddressesForm(forms.Form):
    def __init__(self, queryset, can_copy=False, *args, **kwargs):
        super(UserAddressesForm, self).__init__(*args, **kwargs)
        self.fields['address'] = AddressChoiceField(queryset=queryset,
                                                    can_copy=can_copy)


class ShippingForm(forms.Form):
    method = forms.ChoiceField(label=_('Shipping method'),
                               widget=forms.RadioSelect)

    def __init__(self, delivery_choices, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)
        method_field = self.fields['method']
        method_field.choices = delivery_choices
        if len(delivery_choices) == 1:
            method_field.initial = delivery_choices[0][1]


class AnonymousEmailForm(forms.Form):
    email = forms.EmailField()


def get_form_class_for_service(product):
    from ..product.models import Product
    if isinstance(product, Product):
        return ServiceChoiceForm
    raise NotImplementedError

from ..product.forms import VariantChoiceField

class ServiceChoiceForm(AddToCartForm):
    variant = VariantChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super(ServiceChoiceForm, self).__init__(*args, **kwargs)
        self.fields['variant'].queryset = self.product.variants
        self.fields['variant'].empty_label = None

    def get_variant(self, cleaned_data):
        return cleaned_data.get('variant')

    # queryset=Variations.objects.all(), widget=forms.RadioSelect
    # CHOICES = (('1', 'once'), ('2', 'weekly'), ('3', 'biweekly'))
    # variants = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    # hours  = forms.ChoiceField(choices=[(str(i), '%i hours' %i) for i in range(2, 10)])

