import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from .miband4_func import get_activity_logs, sleeping, sleep_graph, colors
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def user_logout(request):
    logout(request)
    return redirect('home')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'activity/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user, dir(user))
            login(request, user)
            user_save = UserDeviceData(user=user.username)
            user_save.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('entering-device-data')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'activity/register.html', {"form": form})


def entering_device_data_view(request):
    if request.method == 'POST':
        form = UserDeviceDataForm(request.POST)
        if form.is_valid():
            last_user_username = User.objects.order_by('-id')[0].username
            user = UserDeviceData.objects.get(user=last_user_username)
            user.mac_address = form.data['mac_address']
            user.auth_key = form.data['auth_key']
            user.save()
            messages.success(request, 'Данные сохранены')
            return redirect('home')
        else:
            messages.error(request, 'Данные не сохранены')
    else:
        form = UserDeviceDataForm()
    return render(request, 'activity/entering_user_device_data.html', {"form": form})


def index(request):
    articles = Articles.objects.all()
    return render(request, 'activity/index.html', context={'articles': articles, 'title': 'Мониторинг сна'})


def syncs(request):
    username = request.user.username
    user_data = UserDeviceData.objects.filter(user=username)[0]
    with open("activity/current_user.txt", "w") as f:
        f.write(user_data.user)
    if Activity.objects.filter(user=username).exists():
        last_date_time = Activity.objects.order_by('-id')[0].date_time
        start_date_time = datetime.fromtimestamp(last_date_time.timestamp() - 180)
        res = get_activity_logs(
            start_date_time,
            mac_address=user_data.mac_address,
            auth_key=user_data.auth_key
        )
    else:
        last_date_time = datetime.strptime('03.01.2016 16:30:00', "%d.%m.%Y %H:%M:%S")
        res = get_activity_logs(
            last_date_time,
            mac_address=user_data.mac_address,
            auth_key=user_data.auth_key
        )
    if not res:
        messages.error(request, 'Не удалось установить соединение с браслетом. Обновите MAC-адрес и ключ аутентификации')
        return redirect('index')
    else:
        messages.success(request, 'Данные успешно обновлены!')
    return redirect('index')


def one_article(request, article_id):
    article = get_object_or_404(Articles, pk=article_id)
    return render(request, 'activity/article.html', context={'article': article})


def analysis(request):
    print('clicked analysis')
    try:
        print('from try block')
        bruh = Activity.objects.filter(
                date_time=datetime(
                    datetime.now().year,
                    datetime.now().month,
                    datetime.now().day-5,
                    20, 0
                ).strftime("%Y-%m-%d %H:%M:%S"),
                user=request.user.username
        )[0].is_sleeping
    except IndexError:
        print('from except')
        messages.info(request, 'Синхронизируйте данные браслета!')
        return redirect('home')
    if bruh is None:
        print('yeah, babe, bruh is none')
        sleeping(request.user.username)
    count_of_periods = sleep_graph(user=request.user.username)
    index_ = np.arange(16)
    fig = plt.figure(figsize=(8, 2))
    plt.title('Анализ сна за 23.05')
    ax = fig.add_subplot(3, 1, 1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(120))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(60))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_xlabel('Время')
    ax.set_yticklabels(['сон'])
    ax.set_xticklabels(['18', '20', '22', '0', '2', '4', '6', '8', '10'])
    series = []
    for i in range(len(count_of_periods)):
        series.append(count_of_periods[i][1])
    left = 0
    for i in range(len(count_of_periods)):
        ax.barh(index_, series[i], left=left, color=colors[count_of_periods[i][0]])
        left += series[i]
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'activity/analysis.html', context={"graphic": graphic})


def parameters(request):
    if request.method == 'POST':
        form = UserDeviceDataForm(request.POST)
        if form.is_valid():
            UserDeviceData.objects.filter(user=request.user.username).update(
                mac_address=form.data['mac_address'],
                auth_key=form.data['auth_key']
            )
            messages.success(request, 'Данные обновлены')
            return redirect('home')
        else:
            messages.error(request, 'Данные не обновлены')
    else:
        form = UserDeviceDataForm()
    return render(request, 'activity/parameters.html', {"form": form})
