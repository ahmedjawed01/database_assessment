from django.urls import path, include
from populations import views


urlpatterns = [
    path('population/', views.UploadAndDownloadPopulationsCSV.as_view(), name='populations')
]
