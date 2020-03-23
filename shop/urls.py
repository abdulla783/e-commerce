from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('allcategory/', views.allCategory, name="AllCategory"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/<int:id>', views.productView, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
]
