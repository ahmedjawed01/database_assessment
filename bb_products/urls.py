from django.urls import path, include
from bb_products import views


urlpatterns = [
    path('bb-product/', views.UploadAndDownloadBBProductCSV.as_view(), name='bb_product')
]
