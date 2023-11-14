from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('pages-list/', views.PagesListView.as_view(), name='pages_list'),
]