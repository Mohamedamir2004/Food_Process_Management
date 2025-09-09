from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("contact/", views.contact_view, name="contact"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # path('staff/', views.staff_dashboard, name='staff_dashboard'), 
    path('guest-page/', views.guest_page, name='guest_page'), 

     # staff pages
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/add/", views.add_item, name="add_item"),
    path("staff/manage/", views.manage_items, name="manage_items"), 

    # foods CRUD Operations 
    path("add/", views.add_item, name="add_item"),
    path("manage/", views.manage_items, name="manage_items"),
    path("edit/<int:item_id>/", views.edit_item, name="edit_item"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item"),
    
    # Orders
    path('order/', views.guest_page, name="order"),
    # path('cart/add/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.view_cart, name="view_cart"),
    path('checkout/', views.checkout, name="checkout"), 
    # path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'), 
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),

    # cart Crud 
    # path("cart/add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"), 

    # payments
      path("checkout/", views.checkout, name="checkout"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),
]
