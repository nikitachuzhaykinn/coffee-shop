from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    pickup_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label="Время самовывоза",
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'delivery_type', 'address', 'pickup_time']
        widgets = {
            'delivery_type': forms.RadioSelect,
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'delivery_type': 'Тип получения',
            'address': 'Адрес доставки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input = (
            'w-full border border-stone-300 rounded-lg px-4 py-2.5 '
            'focus:outline-none focus:ring-2 focus:ring-amber-800 focus:border-transparent '
            'bg-white transition-all'
        )
        error_input = (
            'w-full border border-red-500 rounded-lg px-4 py-2.5 '
            'focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent '
            'bg-white transition-all'
        )
        for name in ['first_name', 'last_name', 'email', 'phone', 'address', 'pickup_time']:
            if name in self.fields:
                css = error_input if self.errors.get(name) else base_input
                self.fields[name].widget.attrs['class'] = css
                if name in ('first_name', 'last_name', 'email', 'phone'):
                    self.fields[name].widget.attrs['placeholder'] = self.fields[name].label

    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get('delivery_type')
        address = cleaned_data.get('address')
        pickup_time = cleaned_data.get('pickup_time')

        if delivery_type == 'delivery' and not address:
            self.add_error('address', 'Укажите адрес доставки')

        if delivery_type == 'pickup' and not pickup_time:
            self.add_error('pickup_time', 'Укажите время самовывоза')

        return cleaned_data