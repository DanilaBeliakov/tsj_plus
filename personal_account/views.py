from django.shortcuts import redirect, render
from authorization.models import users, houses
# from .forms import AccountForm
from .forms import NewUserForm
import secrets
import string
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.conf import settings

def generate_password():
    alphabet = string.ascii_letters + string.digits + string.ascii_lowercase + string.ascii_uppercase
    password = ''.join(secrets.choice(alphabet) for i in range(8))  # for a 20-character password
    return password



# Create your views here.
def index_account(request):
    user_email = request.session['email']
    user_house = request.session.get('house_id', 1)
    user = users.objects.get(email = user_email)
    role = user.is_admin
    request.session['is_admin'] = role
    house = houses.objects.get(id=user_house)
    address = house.address
    is_admin = request.session.get('is_admin', False)
    return render(request, "base_account.html", context={'email':user_email, 'address': address, 'name': user.full_name, 'is_admin': is_admin})

def new_user_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        flat = request.POST.get('flat_number')
        flat_area = request.POST.get('flat_area')
        flat_share = request.POST.get('flat_flat_share')
        password = generate_password()
        house_id = request.session.get('house_id', 1)
        users.objects.create_user(email, email=email, password=password, is_admin=False, full_name=full_name, flat_number=flat, house_id=house_id)
        send_mail(
            'Регистрация на сервисе ТСЖ Плюс!',
            f'Здравствуйте, {full_name}! Ваш пароль для использования сервиса: {password}. В качестве логина используйте данную почту',
            'tsjplus@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('account/')
        # except IntegrityError:
        #    return HttpResponse(f"<h2>Пользователь с почтой {email} уже ранее регистрировался!</h2>")
        # finally:
        #     pass
    else:
        new_user_form = NewUserForm()
        return render(request, 'new_account.html', context={'form': new_user_form})


def account_logout(request):
    del request.session['is_logged']
    del request.session['email']
    # del request.session['house_id']
    request.session.modified = True
    return redirect('auth')