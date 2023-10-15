from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('category_list/', views.categories, name='category_list'),
    path('add_categories/', views.add_category, name='add_categories'),
    path('delete_category/<str:slug>/',
         views.delete_category, name='delete_category'),
]
