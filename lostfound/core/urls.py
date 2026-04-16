from django.urls import path
from .views import *

urlpatterns = [
    # Home & Search
    path('', home, name='home'),
    
    # Auth
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Items
    path('add/', add_item, name='add_item'),
    path('edit/<int:id>/', edit_item, name='edit_item'),
    path('delete/<int:id>/', delete_item, name='delete_item'),
    path('resolve/<int:id>/', resolve_item, name='resolve_item'),
    
    # Claims
    path('claim/<int:id>/', claim_item, name='claim_item'),
    path('approve/<int:id>/', approve_claim, name='approve_claim'),
    path('reject/<int:id>/', reject_claim, name='reject_claim'),
    
    # Dashboard & Notifications
    path('dashboard/', dashboard, name='dashboard'),
    path('notifications/', notifications, name='notifications'),
]