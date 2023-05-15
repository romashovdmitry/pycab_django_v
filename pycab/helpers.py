from django.conf.urls import handler404
from django.shortcuts import redirect
from django.core.paginator import Paginator

from pycab.settings import DEFAULT_PAGE_SIZE

def custom_404_handler(request, exception=None):
    # Ваш код обработки 404 ошибки здесь
    # Например, вы можете записывать несуществующие URL-адреса в базу данных, отправлять уведомления администратору и т.д.
    pass


def redirect_authenticated_user(func):
    def wrapper(request):

        if request.user.is_authenticated:
            return redirect('table')

    return wrapper

def paginate(request, items, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(items, page_size)
    page_number = request.GET.get("page") or 1
    return paginator.get_page(page_number)