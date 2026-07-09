import json
import numpy as np
import pickle
import pandas as pd
crop_model = pickle.load(
    open(
        'core/ml/model.pkl',
        'rb'
    )
)
yield_model = pickle.load(
    open("core/ml/yield_model.pkl", "rb")
)

state_encoder = pickle.load(
    open("core/ml/state_encoder.pkl", "rb")
)

district_encoder = pickle.load(
    open("core/ml/district_encoder.pkl", "rb")
)

season_encoder = pickle.load(
    open("core/ml/season_encoder.pkl", "rb")
)

crop_encoder = pickle.load(
    open("core/ml/crop_encoder.pkl", "rb")
)
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
disease_model = load_model(
    "core/ml/disease/disease_model.h5"
)

with open(
    "core/ml/disease/labels.txt"
) as f:
    labels = f.read().splitlines()

from .utils import get_coordinates, get_market_price, get_soil_data, get_weather, get_npk, ask_ai

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


def profile(request):
    # ✅ SAFE: profile exist nahi ho toh create ho jayega
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile   # ❗ yaha change
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)  # ❗ yaha change

    return render(request, 'profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# Home
def home(request):
    return render(request, 'home.html')


# Register
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'register.html')


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


#about
def about(request):
    return render(request, 'about.html')

#features
def features(request):
    return render(request, 'features.html')

def safe_transform(encoder, value):
    value = value.strip().upper()

    classes = [x.upper() for x in encoder.classes_]

    if value in classes:
        index = classes.index(value)
        return index

    return 0

def predict(request):
    if request.method == "POST":

        city = request.POST.get('city')
        state = request.POST.get('state')
        district = request.POST.get('district')
        season = request.POST.get('season')
        soil = request.POST.get('soil')
        irrigation = request.POST.get('irrigation')

        if not city:
            return render(request, 'predict.html', {
                'error': 'Enter city'
            })

        # Weather API
        temp, humidity, rainfall = get_weather(city)

        if temp is None:
            return render(request, 'predict.html', {
                'error': 'Invalid city'
            })

        # Soil values
        N, P, K, ph = get_npk(soil)

        # Crop prediction input
        input_data = pd.DataFrame([{
            'N': N,
            'P': P,
            'K': K,
            'temperature': temp,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }])

        # Crop prediction
        crop = crop_model.predict(input_data)[0]
        market, market_state, price = get_market_price(crop)

        # Yield prediction
        state_value = safe_transform(state_encoder, state)
        district_value = safe_transform(district_encoder, district)
        season_value = safe_transform(season_encoder, season)
        crop_value = safe_transform(crop_encoder, crop)

        yield_input = pd.DataFrame([{
            'State_Name': state_value,
            'District_Name': district_value,
            'Season': season_value,
            'Crop': crop_value,
            'Area': 1
        }])

        predicted_yield = round(
            yield_model.predict(yield_input)[0],
            2
        )

        return render(request, 'result.html', {
            'crop': crop,
            'predicted_yield': predicted_yield,
            'temp': temp,
            'humidity': humidity,
            'rainfall': rainfall,
            'city': city,
            'state': state,
            'district': district,
            'season': season,
            'soil': soil,
            'irrigation': irrigation,
            'market': market,
            'market_state': market_state,
            'price': price
        })

    return render(request, 'predict.html')


def chatbot(request):

    if request.method == "POST":

        data = json.loads(
            request.body
        )

        msg = data.get(
            "message"
        )

        lang = data.get(
            "lang",
            "en"
        )

        temp = None
        humidity = None
        city = None
        crops = []

        # City detection
        words = msg.split()

        for word in words:

            if word.istitle():

                city = word
                break

        try:

            if city:

                temp, humidity = get_weather(
                    city
                )

                if temp:

                    crops = (
                        get_crops_by_weather(
                            temp,
                            humidity
                        )
                    )

        except:
            pass

        reply = ask_ai(
            msg,
            (
                temp,
                humidity,
                city
            ),
            crops
        )

        return JsonResponse({
            "reply": reply
        })

def disease_detection(request):

    result = None
    solution = None
    image_url = None
    confidence = None
    healthy = False
    tips = []

    disease_solutions = {

        "Tomato_Early_blight":
        "Use fungicide and remove infected leaves.",

        "Tomato_Late_blight":
        "Avoid overwatering and apply copper spray.",

        "Tomato_Bacterial_spot":
        "Use disease-free seeds and copper fungicides.",

        "Potato_Early_blight":
        "Use proper fungicide treatment.",

        "Potato_Late_blight":
        "Remove infected leaves immediately.",

        "Pepper_bell_Bacterial_spot":
        "Avoid overhead watering and use copper spray.",

        "Tomato__Tomato_mosaic_virus":
        "Remove infected plants and control whiteflies.",

        "Tomato__Tomato_YellowLeaf__Curl_Virus":
        "Use virus-free seedlings and insect control.",

        "Tomato__Leaf_Mold":
        "Improve ventilation and apply fungicide.",

        "Tomato__Septoria_leaf_spot":
        "Remove infected leaves and use fungicide.",

        "Tomato__Spider_mites_Two_spotted_spider_mite":
        "Spray neem oil or miticide.",

        "Tomato__Target_Spot":
        "Apply fungicide and avoid excess moisture.",

        "Tomato_healthy":
        "Plant is healthy. No disease detected.",

        "Potato__healthy":
        "Plant is healthy.",

        "Pepper__bell___healthy":
        "Plant is healthy."
    }

    disease_tips = {

        "Tomato_Early_blight": [
            "Avoid overwatering",
            "Remove infected leaves",
            "Use fungicide"
        ],

        "Tomato_Late_blight": [
            "Keep leaves dry",
            "Avoid extra moisture",
            "Use copper spray"
        ],

        "Tomato__Tomato_mosaic_virus": [
            "Remove infected plants",
            "Control whiteflies",
            "Use clean tools"
        ],

        "healthy": [
            "Continue proper watering",
            "Maintain soil nutrients",
            "Regular monitoring"
        ]
    }

    if request.method == "POST":

        uploaded_file = request.FILES["image"]

        fs = FileSystemStorage()

        filename = fs.save(
            uploaded_file.name,
            uploaded_file
        )

        image_url = fs.url(filename)

        file_path = fs.path(filename)

        img = image.load_img(
            file_path,
            target_size=(128, 128)
        )

        img_array = image.img_to_array(img)

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        img_array = img_array / 255.0

        prediction = disease_model.predict(
            img_array
        )

        predicted_index = np.argmax(
            prediction
        )

        confidence = round(
            np.max(prediction) * 100,
            2
        )

        result = labels[predicted_index]

        result = result.replace("_", " ")

        solution = disease_solutions.get(
            labels[predicted_index],
            "No solution available"
        )

        tips = disease_tips.get(
            labels[predicted_index],
            [
                "Maintain plant hygiene",
                "Regular inspection",
                "Avoid overwatering"
            ]
        )

        if "healthy" in labels[
            predicted_index
        ].lower():
            healthy = True

    return render(
        request,
        "disease.html",
        {
            "result": result,
            "solution": solution,
            "image_url": image_url,
            "confidence": confidence,
            "healthy": healthy,
            "tips": tips
        }
    )

def prediction_options(request):
    return render(
        request,
        'prediction_options.html'
    )