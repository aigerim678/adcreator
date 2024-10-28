
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from uuid import uuid4

from .forms import AudioFileForm
from .forms import VideoFileForm
from .forms import CustomUserCreationForm
from .models import Scenario


def home(request):
    if request.method == 'POST':
        watched = request.POST.get('watched')
        if watched:
            # Логика после просмотра видео
            return redirect('record')
    return render(request, 'home/index.html')


def record(request):
    
    if 'temp_id' not in request.COOKIES:
        temp_id = str(uuid4())
        request.session['temp_id'] = temp_id
    else:
        temp_id = request.COOKIES.get('temp_id')

    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем объект модели, но пока не сохраняем его в базе данных
            audio_file = form.save(commit=False)
            # Проверяем, авторизован ли пользователь
            if request.user.is_authenticated:
                audio_file.user = request.user
                
                audio_file.temp_id = None
            else:
               
                audio_file.temp_id = temp_id
            audio_file.save()
            response = JsonResponse({"status": "success"}, status=200)
            response.set_cookie('temp_id', temp_id)  # Set or update the cookie
            return response
            
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = AudioFileForm()
    return render(request, 'home/record.html', {'form': form})



def script_builder(request):
    return render(request, 'home/script_builder.html')


def write_script(request):

    if 'temp_id' not in request.COOKIES:
        temp_id = str(uuid4())
        request.session['temp_id'] = temp_id
    else:
        temp_id = request.COOKIES.get('temp_id')

    if request.method == "POST":
        scenario_text = request.POST.get("scenario_text")
        if scenario_text:
            if request.user.is_authenticated:
                # Link the scenario to the authenticated user
                scenario = Scenario.objects.create(text=scenario_text, user=request.user, temp_id=None)
            else:
                # Link the scenario to the session using temp_id
                scenario = Scenario.objects.create(text=scenario_text, temp_id=temp_id)
            print("Scenario saved with ID:", scenario.id)
            response = redirect("record")
            response.set_cookie('temp_id', temp_id)  # Set or update the temp_id cookie
            return response
    return render(request, 'home/write_script.html')


def use_template(request):

    if 'temp_id' not in request.COOKIES:
        temp_id = str(uuid4())
        request.session['temp_id'] = temp_id
    else:
        temp_id = request.COOKIES.get('temp_id')

    if request.method == "POST":
        # Получаем данные из текстовых областей
        loud_start = request.POST.get("loud_start")
        text_amplifier = request.POST.get("text_amplifier")
        main_text = request.POST.get("main_text")
        call_to_action = request.POST.get("call_to_action")

        # Объединяем текст для сценария
        scenario_text = f"{loud_start}\n\n{text_amplifier}\n\n{main_text}\n\n{call_to_action}"

        if scenario_text:
            if request.user.is_authenticated:
                # Link the scenario to the authenticated user
                scenario = Scenario.objects.create(text=scenario_text, user=request.user, temp_id=None)
            else:
                # Link the scenario to the session using temp_id
                scenario = Scenario.objects.create(text=scenario_text, temp_id=temp_id)
            print("Scenario saved with ID:", scenario.id)
            response = redirect("record")
            response.set_cookie('temp_id', temp_id)  # Set or update the temp_id cookie
            return response
    return render(request, 'home/use_template.html')



def video_step(request):
    
    if 'temp_id' not in request.COOKIES:
        temp_id = str(uuid4())
        request.session['temp_id'] = temp_id
    else:
        temp_id = request.COOKIES.get('temp_id')

    if request.method == 'POST':
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            video_file = form.save(commit=False)
            # Проверяем, авторизован ли пользователь
            if request.user.is_authenticated:
                video_file.user = request.user
                
                video_file.temp_id = None
            else:
                
                video_file.temp_id = temp_id
            video_file.save()
            response = JsonResponse({"status": "success"}, status=200)
            response.set_cookie('temp_id', temp_id) 
            return response
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = VideoFileForm()
    return render(request, 'home/video_step.html', {'form': form})







def user_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()
            # Логиним пользователя после успешной регистрации
            login(request, user)
            return redirect('login') 
        else:
            # Если форма не валидна, возвращаем ответ с ошибками
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        # Если запрос GET, создаем пустую форму регистрации
        form = CustomUserCreationForm()

    return render(request, 'home/index.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('home')  
            else:
                # Если аутентификация не прошла
                return JsonResponse({"status": "error", "errors": {"non_field_errors": ["Неверное имя пользователя или пароль."]}}, status=400)
        else:
            # Если форма не валидна, возвращаем ответ с ошибками
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = AuthenticationForm()

    return render(request, 'home/index.html', {'form': form})



@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('home'))



import re



def parse_response(response_text):

    variants = re.split(r'Вариант \d+', response_text)

    # Оставляем только непустые строки и убираем ведущие/замыкающие пробелы
    variants = [variant.strip() for variant in variants if variant.strip()]

    variants_blocks = [variant.split('\n\n') for variant in variants]

    # Возвращаем список вариантов
    return variants_blocks


import os
from dotenv import load_dotenv
from groq import Groq

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

groq_api_key = os.getenv("GROQ_API_KEY")

def generate_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        source = request.POST.get('source', 'write_script')

        if not user_message:
            return render(request, f'home/{source}.html', {"error": "Введите сообщение."})
        
        # Инициализация клиента Groq
        client = Groq(api_key=groq_api_key)

        # Создание completion
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "\"Напиши три варианта ответа в пяти блоках на тему который указан в user message. Ответ должен быть информативным, поддерживающим и убедительным. Упомяни меры безопасности, предпринятые для защиты клиентов, приведи примеры услуг, которые мы предоставляем, и подчеркни профессионализм мастеров. Не забывай добавить призыв к действию в конце каждого варианта.\"\n\nПример ответа\n\nВариант 1\n\nМы работаем для вас даже в самые сложные времена!\n\nНаша компания не прекращала работу во время карантина, чтобы вы могли быть уверены в надёжности своего автомобиля. Мы заботимся о безопасности и комфорте наших клиентов, поэтому соблюдаем все необходимые меры предосторожности.\n\nНаши мастера прошли дополнительную подготовку по работе в условиях пандемии, а также используют средства индивидуальной защиты. Это позволяет нам гарантировать безопасность и качество предоставляемых услуг.\n\nМы предлагаем широкий спектр услуг по ремонту и обслуживанию автомобилей различных марок и моделей. Наши специалисты имеют большой опыт работы и готовы решить любую проблему с вашим автомобилем.\n\nНе рискуйте безопасностью и комфортом — доверьте свой автомобиль профессионалам!\n\nВариант 2\n\nКак мы работали во время карантина\n\nВ это непростое время многие компании были вынуждены приостановить свою деятельность. Но только не мы! Наша компания продолжала работать, чтобы обеспечить вам качественный сервис и поддержку.\n\nВо время карантина мы приняли дополнительные меры безопасности, чтобы защитить наших сотрудников и клиентов. Мы следим за соблюдением всех необходимых мер предосторожности, включая использование средств индивидуальной защиты и регулярную дезинфекцию помещений.\n\nНесмотря на все трудности, мы продолжаем предоставлять вам высококачественные услуги по ремонту и техническому обслуживанию автомобилей. Наши мастера имеют большой опыт и знания, которые позволяют им быстро и эффективно решать любые проблемы с вашим авто.\n\nЕсли у вас возникли вопросы или нужна помощь, обращайтесь к нам. Мы всегда готовы помочь!\n\nВариант 3\n\nРабота автосервиса во время карантина: как мы обеспечиваем вашу безопасность\n\nКарантин стал настоящим испытанием для многих компаний. Однако наша компания продолжает работать, чтобы предоставить вам качественные услуги и поддержку.\n\nМы понимаем, что в это непростое время важно соблюдать все меры предосторожности. Поэтому мы приняли ряд дополнительных мер безопасности, чтобы защитить вас и наших сотрудников.\n\nВсе наши мастера проходят дополнительную подготовку по работе в условиях карантина. Они используют средства индивидуальной защиты, регулярно дезинфицируют помещения и инструменты.\n\nКроме того, мы строго следим за тем, чтобы все клиенты соблюдали социальную дистанцию и использовали средства индивидуальной защиты при посещении нашего сервиса.\n\nДоверьте свой автомобиль нам, и мы позаботимся о его безопасности и надёжности!"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Создание ответа
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""

        # Разбиваем на варианты
        variants = parse_response(response_text)

        # Передаем результат обратно в шаблон
        return render(request, f'home/{source}.html', {"variants": variants})

    # Обработка GET-запроса (например, при первом отображении формы)
    return render(request, f'home/{source}.html')






from .models import AudioFile, UploadedVideo
from django.contrib.auth import get_user_model

User = get_user_model()
audio_file_url = ''
video_file_url = ''
def process_files_for_user(user_id):
    global audio_file_url, video_file_url
    try:
        user = User.objects.get(id=user_id)
        audio_file = AudioFile.objects.filter(user=user).last()
        video_file = UploadedVideo.objects.filter(user=user).last()

        if not audio_file or not video_file:
            print("Аудио или видео файл не найден.")
        else:
            print(f"Audio File: {audio_file.file.url if audio_file else 'None'}")
            print(f"Video File: {video_file.video.url if video_file else 'None'}")
            audio_file_url = audio_file.file.url
            video_file_url = video_file.video.url

    except User.DoesNotExist:
        print("Пользователь с таким ID не найден.")



import os
import time
from dotenv import load_dotenv
import requests

def generate_video(user_id):
    # Вызываем функцию для получения URL файлов пользователя
    process_files_for_user(user_id)

    # Проверяем, что URL установлены
    if not audio_file_url or not video_file_url:
        print("Не удалось получить URL для аудио или видео файла.")
        return

    # Загрузка API ключа из .env файла
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)

    video_api_key = os.getenv("VIDEO_API_KEY")

    if not video_api_key:
        print("Ошибка: API ключ не найден.")
        return

    # Начальный запрос на генерацию видео
    url = "https://api.sync.so/v2/generate"
    payload = {
        "model": "lipsync-1.7.1",
        "input": [
            {
                "type": "video",
                "url": video_file_url
            },
            {
                "type": "audio",
                "url": audio_file_url
            }
        ],
        "options": {"output_format": "mp4"}
    }

    headers = {
        "x-api-key": video_api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Проверка статуса запроса
    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}, {response.text}")
        return

    # Получаем ID задачи из ответа
    response_data = response.json()
    task_id = response_data.get("id")

    if not task_id:
        print("Ошибка: Не удалось создать задачу.")
        return

    # URL для опроса статуса задачи
    polling_url = f"https://api.sync.so/v2/generate/{task_id}"

    while True:
        # Опрос API для получения статуса задачи
        poll_response = requests.get(polling_url, headers=headers)
        poll_data = poll_response.json()

        status = poll_data.get("status")

        if status == "COMPLETED":
            # Задача завершена успешно
            output_url = poll_data.get("outputUrl")
            print("Видео успешно сгенерировано:", output_url)
            return output_url
        elif status == "FAILED":
            # Произошла ошибка
            error = poll_data.get("error")
            print("Ошибка при генерации видео:", error)
            return
        else:
            # Задача все еще обрабатывается, подождем 5 секунд
            print("Задача все еще обрабатывается...")
            time.sleep(5)