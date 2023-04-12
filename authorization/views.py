from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import SignUpForm
from .forms import AuthForm
from .models import users
from .models import houses
from django.db import IntegrityError
from django.contrib.auth import authenticate


def sign_up_page(request):
    if request.method == "POST":
        # получение данных из POST-запроса на регистрацию
        form = SignUpForm(request.POST)
        name = request.POST.get("full_name")
        email = request.POST.get('email')
        address = request.POST.get('address')
        flat = request.POST.get('flat_number')
        password = request.POST.get('password_first')
        flat_area = request.POST.get('flat_area')
        flat_share = eval(request.POST.get('flat_share'))
        is_admin = 1
        new_address = houses.objects.create(address=address)
        house_id = new_address.id
        try:
            users.objects.create_user(username=email, email=email, password=password, house_id=house_id, flat_number=flat, full_name=name, is_admin=is_admin, flat_area=flat_area, flat_share=flat_share)
            request.session['email'] = email
            request.session['is_logged'] = True
            request.session['house_id'] = house_id
            request.session['is_admin'] = True
            request.session.modified = True
            return redirect('/news/')
        except IntegrityError:
           return HttpResponse(f"<h2>Пользователь c почтой {email} уже ранее регистрировался!</h2>")
    else:
        # обработка GET-запроса для получения страницы регистрации
        userform = SignUpForm()
        return render(request, "signup.html", {"form": userform})


def auth_page(request):
    if request.method == "POST":
        # получение данных из POST-запроса на авторизацию
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            address = houses.objects.get(id=user.house_id)
            request.session['email'] = email
            request.session['is_logged'] = True
            request.session['house_id'] = user.house_id
            request.session.modified = True
            return redirect('/news/')
        else:
            return HttpResponse(f"<h2>Авторизация не удалась, пользователь c такой почтой и паролем не найден!")
    else:
        # обработка GET-запроса для получения страницы регистрации
        userform = AuthForm()
        is_logged = request.session.get('is_logged', False)
        if is_logged:
            return redirect('/news/')
        else:
            return render(request, "auth.html", {"form": userform})
