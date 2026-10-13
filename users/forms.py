from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from .models import Address, Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': 'email@example.com'
        })
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': '+7 (999) 999-99-99'
        }),
        required=True,
        error_messages={
            'required': 'Введите номер телефона',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Имя пользователя'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['username'].help_text = "Обязательно. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."
        self.fields['username'].error_messages = {
            'required': 'Введите имя пользователя',
            'unique': 'Пользователь с таким именем уже существует',
        }
        
        self.fields['email'].label = "Email"
        self.fields['email'].help_text = ""
        self.fields['email'].error_messages = {
            'required': 'Введите email',
            'invalid': 'Введите корректный email',
            'unique': 'Пользователь с таким email уже существует',
        }
        
        self.fields['password1'].label = "Пароль"
        self.fields['password1'].help_text = mark_safe(
            "Ваш пароль должен содержать как минимум 8 символов.<br>"
            "Пароль не должен быть слишком простым или похожим на личную информацию.<br>"
            "Пароль не должен быть широко распространённым.<br>"
            "Пароль не должен состоять только из цифр."
        )
        self.fields['password1'].error_messages = {
            'required': 'Введите пароль',
        }
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': 'Пароль'
        })
        
        self.fields['password2'].label = "Подтверждение пароля"
        self.fields['password2'].help_text = "Введите тот же пароль, что и выше, для проверки."
        self.fields['password2'].error_messages = {
            'required': 'Подтвердите пароль',
            'password_mismatch': 'Пароли не совпадают',
        }
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': 'Подтвердите пароль'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Введите email адрес')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or not phone.strip():
            raise ValidationError('Введите номер телефона')
        return phone.strip()

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Имя пользователя или Email",
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': 'Введите имя пользователя или email'
        }),
        error_messages={
            'required': 'Введите имя пользователя или email',
        }
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': 'Пароль'
        }),
        error_messages={
            'required': 'Введите пароль',
        }
    )

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
            'placeholder': '+7 (999) 999-99-99'
        }),
        error_messages={
            'required': 'Введите номер телефона',
        }
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'email@example.com'
            }),
        }
        error_messages = {
            'first_name': {'required': 'Введите имя'},
            'last_name': {'required': 'Введите фамилию'},
            'email': {
                'required': 'Введите email',
                'invalid': 'Введите корректный email',
            }
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip():
            raise ValidationError('Введите имя')
        return first_name.strip()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip():
            raise ValidationError('Введите фамилию')
        return last_name.strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Введите email')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or not phone.strip():
            raise ValidationError('Введите номер телефона')
        return phone.strip()

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('title', 'city', 'street', 'building', 'apartment', 'phone', 'is_default')
        labels = {
            'title': 'Название',
            'city': 'Город',
            'street': 'Улица',
            'building': 'Дом',
            'apartment': 'Квартира',
            'phone': 'Телефон',
            'is_default': 'Адрес по умолчанию',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Дом, Офис'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Город'
            }),
            'street': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Улица'
            }),
            'building': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Дом'
            }),
            'apartment': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': 'Квартира (необязательно)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-stone-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-800 bg-white',
                'placeholder': '+7 (999) 999-99-99'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-amber-800 border-stone-300 rounded focus:ring-amber-800'
            }),
        }
        error_messages = {
            'title': {'required': 'Введите название адреса'},
            'city': {'required': 'Введите город'},
            'street': {'required': 'Введите улицу'},
            'building': {'required': 'Введите номер дома'},
            'phone': {'required': 'Введите телефон'},
        }