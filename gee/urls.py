from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('map/', views.map_view, name='map'),
    path('get-image-collection', views.get_image_collection, name='get-image-collection'),
    path('test1/',views.test1,name='test1')
]