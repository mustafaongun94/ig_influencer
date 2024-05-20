from django.urls import path
from .views import influencer_list, influencer_detail, influencer_add, influencer_delete


urlpatterns = [
    path('', influencer_list, name='influencer_list'),
    path('add/', influencer_add, name='influencer_add'),
    path('delete/<int:pk>/', influencer_delete, name='influencer_delete'),
    path('<int:pk>/', influencer_detail, name='influencer_detail'),
]