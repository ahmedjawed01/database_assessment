from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from custom_user import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('bb-product-login/', views.CustomLoginView.as_view(), name='bb_login'),
    path('population-login/', views.CustomLoginView.as_view(), name='pop_login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', TemplateView.as_view(template_name='index.html'), name='index')
]
