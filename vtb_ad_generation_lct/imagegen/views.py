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

        channel = request.POST.get('channel')
        category = request.POST.get('category')
        product = request.POST.get('product')

        with open(os.path.join('static/', random.choice(os.listdir('./static'))), 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        image = Image.objects.create(session=session, channel=channel, category=category, product=product,
                                     image=encoded_image)

        return JsonResponse(
            {"image": image.image, "channel": image.channel, "category": image.category, "product": image.product},
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
