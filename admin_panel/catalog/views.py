from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES для загрузки изображений
        if form.is_valid():  # Проверка формы на корректность
            form.save()  # Сохранение в базу данных
            return redirect('/catalog')  # Перенаправление после успешного добавления
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
    

def catalog(request):
    return render(request, 'product_list.html')