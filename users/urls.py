from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('profile/address/add/', views.add_address, name='add_address'),
    path('profile/address/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('profile/address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
]