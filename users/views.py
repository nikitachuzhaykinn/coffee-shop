from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, ProfileForm, AddressForm
from .models import Address, Profile
from orders.models import Order

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем пользователя (сигнал в models.py автоматически создаст для него пустой Profile)
            user = form.save()
            
            # 2. Безопасно получаем существующий профиль или создаем новый (если сигнала нет)
            profile, created = Profile.objects.get_or_create(user=user)
            
            # 3. Обновляем телефон в профиле
            phone = form.cleaned_data.get('phone')
            if phone:
                profile.phone = phone
                profile.save()
            
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('users:profile')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            user = None
            
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:
                user = authenticate(request, username=username_or_email, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'users:profile')
                messages.success(request, 'Вы успешно вошли!')
                return redirect(next_url)
            else:
                form.add_error(None, 'Неверный пароль или пользователь не найден')
        return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('catalog:product_list')

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    addresses = Address.objects.filter(user=request.user)
    
    # Получаем или создаём профиль
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Сохраняем телефон в профиль
            phone = request.POST.get('phone', '')
            profile.phone = phone
            profile.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
        form.fields['phone'].initial = profile.phone
    
    return render(request, 'users/profile.html', {
        'form': form,
        'orders': orders,
        'addresses': addresses,
        'profile': profile
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'users/order_detail.html', {'order': order})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Адрес добавлен')
            return redirect('users:profile')
    else:
        form = AddressForm()
    return render(request, 'users/address_form.html', {'form': form, 'title': 'Добавить адрес'})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Адрес обновлен')
            return redirect('users:profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/address_form.html', {'form': form, 'title': 'Редактировать адрес'})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Адрес удален')
    return redirect('users:profile')