# built-in django packages
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import TemplateView, FormView, View
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

# custom django classes
from table.forms import AuthForm
from users.models import MyUser, UserInfo

# custom classes
from table.backendAndTelegram.hash import hashing
from pycab.helpers import redirect_authenticated_user
import logging

# redis
from table.tasks import py_send_mail

# etc libs
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Registration(FormView, View):

    template_name = 'auth_pages/user_register.html'
    form_class = AuthForm
    success_url = reverse_lazy('infopage')

    @method_decorator(redirect_authenticated_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        form = self.form_class(request.POST)

        print(2)

        if form.is_valid():

            print(3)

            user = form.save(commit=False)
            print(4)
            user.email = user.email.lower()
            user.password = hashing(user.password)
            user.save()
            login(request, user)
            print(5)
            new_user_info = UserInfo()
            new_user_info.user_email = user
            new_user_info.save()
            print(6)
            messages.info(request, f'Account for {user.email} is added!')
            return self.form_valid(self.form_class)

        else:

#            messages.error(request, "anything go wrong :( Please, try again. ")
            messages.error(request, f"{form.errors}")
            return render(request, 'auth_pages/user_register.html', {'form': self.form_class})

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('table')

        return render(
            request,
            self.template_name,
            {
                'form': self.form_class
            }
        )


class Login(FormView, View):

    template_name = 'auth_pages/user_login.html'
    form_class = AuthForm()

    @method_decorator(redirect_authenticated_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        email = request.POST.get('email').lower()

        if MyUser.objects.filter(email=email).exists():

            password = request.POST.get('password')
            user = MyUser.objects.get(email=email)
            true_password = user.password
            if hashing(password) == true_password:
                login(request, user)
                return redirect('table')
            else:
                messages.error(request, "Wrong password :(")
        else:
            messages.error(request, "Didn't find this email :(")
        return render(
            request,
            self.template_name,
            {'form': self.form_class}
        )

    def get(self, request):

        return render(
            request,
            self.template_name,
            {'form': self.form_class}
        )


def password_step_first(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        if MyUser.objects.filter(email=em).exists():
            request.session['email-for-user'] = em
            password = MyUser.objects.filter(email=em).first().password
            fake_password = str(password[:10])[::-1]
            request.session['fake_password'] = fake_password
            py_send_mail.delay(
                adress=em, code=fake_password)
            return render(request, 'password_step_second.html')
        else:
            return HttpResponse(f'ther is no this email: {em}')
    return render(request, 'password_step_first.html')


def password_step_second(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        fake_password = request.session['fake_password']
        em = request.session['email-for-user']
        if password == fake_password:
            #            del request.session['fake_password']
            return render(request, 'password_step_lust.html')
    return HttpResponse('nope')


def password_step_lust(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        new_password = hashing(new_password)
        em = request.session['email-for-user']
        user = MyUser.objects.get(email=em)
        user.password = new_password
        user.save()
        login(request, user)
        messages.info(request, f'Password for {user.email} is modified!')
        return redirect('login')


class InfoPage(TemplateView):

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'infopage.html'


def logout(request):
    user_logout(request)
    return redirect('login')
