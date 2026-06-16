from django.urls import path
from . import views

app_name = "shopapp"

urlpatterns = [
    path('', views.index, name = "main"),
    path('login/', views.UserLogin.as_view(), name = "login" ),
    path('main/',views.main, name="main"),
    path('registerUser/', views.UserRegister.as_view(), name = "register_user"),
    path('registerUserConfirm/', views.UserRegisterConfirm.as_view(), name = "register_user_confirm"),
    path('logout/', views.logoutview, name="logout"),
    path('userInfo/',views.user_info, name = "user_info"),
    path('updateUser/',views.UserUpdate.as_view(), name = "update_user"),
    path('updateUserConfirm/', views.UserUpdateConfirm.as_view(), name = "update_user_confirm"),
    path('withdraw/', views.withdraw, name = "withdraw"),
    path('withdrawConfirm/', views.withdrawConfirm, name = "withdraw_confirm"),
    path('searchResult/', views.searchResult, name = "search_result"),
    path('itemDetail/<int:pk>', views.itemDetail, name = "item_detail"),
    path('Cart/',views.shoppingCart, name = "cart")




]