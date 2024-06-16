# imagegen/views.py
import os.path
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserLoginForm
from .models import Session, Image
import base64

from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('generate_image')
    else:
        form = UserRegistrationForm()
    return render(request, 'imagegen/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('generate_image')
    else:
        form = UserLoginForm()
    return render(request, 'imagegen/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def generate_image(request):
    sessions = Session.objects.filter(user=request.user).order_by('-created_at')[:5]
    if len(sessions) == 0:
        return redirect('create_session')

    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        if not session_id.isdigit():
            session_id = sessions[0].id
        session = Session.objects.get(id=session_id)

        def get_float_or_none(data, key):
            value = data.get(key)
            value = value.replace(',', '.')
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        image_source = request.POST.get('image_source')

        channel = request.POST.get('channel')
        product = request.POST.get('product')

        gender = get_float_or_none(request.POST, 'gender')
        age = get_float_or_none(request.POST, 'age')
        cnt_tr_all_3m = get_float_or_none(request.POST, 'cnt_tr_all_3m')
        cnt_tr_top_up_3m = get_float_or_none(request.POST, 'cnt_tr_top_up_3m')
        cnt_tr_cash_3m = get_float_or_none(request.POST, 'cnt_tr_cash_3m')
        cnt_tr_buy_3m = get_float_or_none(request.POST, 'cnt_tr_buy_3m')
        cnt_tr_mobile_3m = get_float_or_none(request.POST, 'cnt_tr_mobile_3m')
        cnt_tr_oil_3m = get_float_or_none(request.POST, 'cnt_tr_oil_3m')
        cnt_tr_on_card_3m = get_float_or_none(request.POST, 'cnt_tr_on_card_3m')
        cnt_tr_service_3m = get_float_or_none(request.POST, 'cnt_tr_service_3m')
        sum_zp_12m = get_float_or_none(request.POST, 'sum_zp_12m')
        app_vehicle_ind = get_float_or_none(request.POST, 'app_vehicle_ind')

        with open(os.path.join('static/', random.choice(os.listdir('./static'))), 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        image = Image.objects.create(session=session, channel=channel, product=product, gender=gender,
                                     age=age, cnt_tr_all_3m=cnt_tr_all_3m, cnt_tr_top_up_3m=cnt_tr_top_up_3m,
                                     cnt_tr_cash_3m=cnt_tr_cash_3m, cnt_tr_buy_3m=cnt_tr_buy_3m,
                                     cnt_tr_mobile_3m=cnt_tr_mobile_3m, cnt_tr_oil_3m=cnt_tr_oil_3m,
                                     cnt_tr_on_card_3m=cnt_tr_on_card_3m, cnt_tr_service_3m=cnt_tr_service_3m,
                                     sum_zp_12m=sum_zp_12m, app_vehicle_ind=app_vehicle_ind,
                                     image=encoded_image)

        return JsonResponse(
            {"image": image.image, "channel": image.channel, "product": image.product,
             "gender": image.gender, "age": image.age, "cnt_tr_all_3m": image.cnt_tr_all_3m,
             "cnt_tr_top_up_3m": image.cnt_tr_top_up_3m, "cnt_tr_cash_3m": image.cnt_tr_cash_3m,
             "cnt_tr_buy_3m": image.cnt_tr_buy_3m, "cnt_tr_mobile_3m": image.cnt_tr_mobile_3m,
             "cnt_tr_oil_3m": image.cnt_tr_oil_3m, "cnt_tr_on_card_3m": image.cnt_tr_on_card_3m,
             "cnt_tr_service_3m": image.cnt_tr_service_3m, "sum_zp_12m": image.sum_zp_12m,
             "app_vehicle_ind": image.app_vehicle_ind},
            status=200)

    selected_session_id = request.GET.get('session_id')

    if not selected_session_id or not selected_session_id.isdigit():
        selected_session_id = sessions[0].id
    selected_session_id = int(selected_session_id)

    try:
        selected_session = Session.objects.get(id=selected_session_id)
        images = Image.objects.filter(session=selected_session)
    except Session.DoesNotExist:
        selected_session = None
        images = []

    return render(request, 'imagegen/generate_image.html', {'sessions': sessions, 'images': images[::-1]})


@login_required
def create_session(request):
    Session.objects.create(user=request.user)
    return redirect('generate_image')
