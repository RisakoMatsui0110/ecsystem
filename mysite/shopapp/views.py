from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from shopapp.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, SearchForm
from shopapp.models import User, Item, Category, Cart
from . import models
from django.contrib.auth import logout
from django.db.models import Q

def index(request):
    request.session['is_login'] = False
    return render(request, "shopapp/main.html")

def login(request):
    return render(request, "shopapp/login.html")

class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        context = {
                "form" : form,
            }
        return render(request, "shopapp/login.html", context)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if not form.is_valid():
            context ={
                "form" : form
            }
            return render(request,"shopapp/login.html", context)
        
        login_user =  User.objects.filter(user_id = form.cleaned_data.get("id")).first()
        request.session['is_login'] = True
        request.session['name'] = login_user.name
        request.session['id'] = login_user.user_id
        request.session['address'] = login_user.address
        request.session['password'] = login_user.password
        context={
            "is_login" : request.session['is_login'],
            "name" :request.session['name'],
        }
        
        
        return render(request,"shopapp/main.html",context)

def main(request):
    if request.session.get("is_login") == True:
        context = {
            "is_login": request.session["is_login"],
            "name" :request.session['name'],
        }
        return render(request, "shopapp/main.html",context)
    else:
        return render(request, "shopapp/main.html")
    
def searchResult(request):
    selected_category = request.POST['category']
    keyword = request.POST['keyword']
    if selected_category == "all":
        category = "すべて"
        if keyword == "":
            search_item =Item.objects.all()
        else:
            search_item =Item.objects.filter(Q(name__icontains=keyword) | Q(manufacturer__icontains = keyword))
    else:
        category = Category.objects.filter(category_id = selected_category).first()
        category = category.name
        if keyword =="":
            search_item =Item.objects.filter(category_id=selected_category)
        else:
            search_item =Item.objects.filter(Q(category_id=selected_category)& ( Q(name__icontains=keyword) | Q(manufacturer__icontains = keyword)))

    context = {
        "search_item" : search_item,
        "category" : category,
        "keyword" : keyword,
    }
    
    return render(request,"shopapp/searchResult.html", context)

def itemDetail(request, pk):
    item = Item.objects.get(item_id = pk)
    context = {
        "is_login": request.session['is_login'],
        "item" :item,
        "numbers": range(1, 11) 
    }
    return render(request,"shopapp/itemDetail.html", context)

def shoppingCart(request):
    if request.method == "GET":
        if request.session['is_login'] == True:
            cart_items = Cart.objects.filter(user_id = request.session["id"])
            total_price = 0
            for cart in cart_items:
                total_price += cart.item.price * cart.amount
            context = {
                "cart_items" : cart_items,
                "total_price" :total_price
            }
            return render(request,"shopapp/cart.html", context)
        return render(request,"shopapp/cart.html")

    if request.method == "POST":
        item_id = request.POST['item_id']
        num = request.POST['num']
        item = Item.objects.get(item_id = item_id)
        user = User.objects.get(user_id = request.session["id"])
        add_item = Cart()
        add_item.amount = num
        add_item.item = item
        add_item.user = user
        add_item.save()

        cart_items = Cart.objects.filter(user_id = request.session["id"])
        total_price = 0
        for cart in cart_items:
            total_price += cart.item.price * cart.amount

        context = {
            "cart_items" : cart_items,
            "total_price" :total_price
        }

        return render(request,"shopapp/cart.html", context)


def logoutview(request):
    logout(request)
    return redirect(reverse("shopapp:login"))
        

class UserRegister(View):
    def get(self, request):
        form = UserRegisterForm()
        context ={
                "form" : form
            }
        return render(request, "shopapp/registerUser.html", context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            context ={
                "form" : form
            }
            return render(request,"shopapp/registerUser.html", context)
        
        context = {
            "register_user" : form.cleaned_data,
        }
        return render(request, "shopapp/registerUserConfirm.html",context)
    
class UserRegisterConfirm(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            context ={
                "form" : form
            }
            return render(request,"shopapp/registerUser.html", context)
        
        register_user = User()
        register_user.user_id = form.cleaned_data["user_id"]
        register_user.password = form.cleaned_data["password1"]
        register_user.name = form.cleaned_data["name"]
        register_user.address = form.cleaned_data["address"]    
        register_user.save()
        context = {
            "register_user" : register_user,
        }
        
        return render(request,"shopapp/registerUserCommit.html", context)

def user_info(request):
    queryset = models.User.objects.filter(user_id = request.session['id']).first()   
    context ={
                "queryset" : queryset
            }
    return render(request, "shopapp/userinfo.html", context)

class UserUpdate(View):
    def get(self, request):
        current_user = User.objects.filter(user_id = request.session["id"]).first()

        form = UserUpdateForm(
            initial={
                "user_id": current_user.user_id,
                "password1": current_user.password,
                "password2": current_user.password,
                "name": current_user.name,
                "address": current_user.address,
            },
            original_user_id=current_user.user_id
        )

        context ={
                "form" : form
            }
        return render(request, "shopapp/updateUser.html", context)
    
    def post(self, request):
        current_user = User.objects.filter(user_id=request.session["id"]).first()

        form = UserUpdateForm(
            request.POST,
            original_user_id=current_user.user_id
        )

        if not form.is_valid():
            context ={
                "form" : form
            }
            return render(request,"shopapp/updateUser.html", context)
        
        context = {
            "update_user" : form.cleaned_data,
        }
        return render(request,"shopapp/updateUserConfirm.html", context)

class UserUpdateConfirm(View):
    def post(self, request):
        current_user = User.objects.get(user_id=request.session["id"])
        form = UserUpdateForm(
            request.POST,
            original_user_id=current_user.user_id
        )

        if not form.is_valid():
            context ={
                
                "form" : form
            }
            return render(request,"shopapp/updateUser.html", context)
        
        
        current_user.user_id = form.cleaned_data["user_id"]
        current_user.password = form.cleaned_data["password1"]
        current_user.name = form.cleaned_data["name"]
        current_user.address = form.cleaned_data["address"]
        current_user.save()

        
        request.session["id"] = current_user.user_id
        request.session["password"] = current_user.password
        request.session["name"] = current_user.name
        request.session["address"] = current_user.address


        context = {
            "update_user" : current_user,
        }
        return render(request,"shopapp/updateUserCommit.html", context)
    
def withdraw(request):
    context = {
        "name" :request.session['name']
    }
    return render(request, "shopapp/withdrawConfirm.html",context)


def withdrawConfirm(request):
    if request.method == "POST":
        current_user = User.objects.filter(user_id=request.session["id"]).first()
        user_name = current_user.name
        current_user.delete()
        context = {
            "user_name" : user_name
        }
        return render(request,"shopapp/withdrawCommit.html", context)

