from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES для загрузки изображений
        if form.is_valid():  # Проверка формы на корректность
            form.save()  # Сохранение в базу данных
            return redirect('catalog')  # Перенаправление после успешного добавления
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})
    

def catalog(request):
    products = Product.objects.all()  # Получаем все товары
    return render(request, 'catalog/product_list.html', {'products': products})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'catalog/add_category.html', {'form': form})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Перенаправление после сохранения
    
    else:
        form = CategoryForm(instance=category)  # Заполняем форму текущими данными
    
    return render(request, 'catalog/edit_category.html', {'form': form, 'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    
    return render(request, 'catalog/delete_category.html', {'category': category})
       

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/category_list.html', {'categories': categories})


def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required  # Доступ только авторизованным
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser and user != request.user:  # Только админ может удалять | # Нельзя удалить себя
        user.delete()
    
    return redirect('user_list')