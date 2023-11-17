from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('pages-list/', views.PagesListView.as_view(), name='pages_list'),
    path('diary-detail/<int:pk>',views.PagesDetailView.as_view(), name='pages_detail'),
    path('pages-create/', views.PagesCreateView.as_view(), name='pages_create'),
    path('pages-update/<int:pk/', views.PagesUpdateView.as_view(), name='pages_update'),
]