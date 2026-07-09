import requests
API_KEY = "99d78dc092c2d3b84e994f0533b82c20"

# ---------------- WEATHER ----------------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'main' not in data:
        return None, None, None

    temp = data['main']['temp']
    humidity = data['main']['humidity']
    rainfall = data.get('rain', {}).get('1h', 0)

    return temp, humidity, rainfall

def get_npk(soil):

    if soil == "Alluvial":
        return 90, 40, 40, 6.5

    elif soil == "Black":
        return 70, 60, 50, 7.2

    elif soil == "Red":
        return 50, 40, 40, 5.8

    elif soil == "Laterite":
        return 40, 30, 30, 5.5

    elif soil == "Mountain":
        return 45, 35, 35, 6.0

    else:
        return 50, 40, 40, 7.0

def get_coordinates(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return None, None

    lat = data['coord']['lat']
    lon = data['coord']['lon']

    return lat, lon

def get_soil_data(lat, lon):

    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
        f"lat={lat}&lon={lon}"
        "&property=phh2o"
        "&property=nitrogen"
        "&property=clay"
        "&property=sand"
        "&depth=0-5cm"
        "&value=mean"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soil_data = response.json()

    return soil_data

API_KEY_DATA = "579b464db66ec23bdd000001e486295a45e4471149378d2d404af38a"

def get_market_price(crop):

    url = (
        "https://api.data.gov.in/resource/"
        "9ef84268-d588-465a-a308-a864a43d0070"
        f"?api-key={API_KEY_DATA}"
        "&format=json"
        "&limit=1"
        f"&filters[commodity]={crop}"
    )

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return "Unknown", "Unknown", "Not Available"

        market_data = response.json()
        print(market_data)

        # Agar records empty hain
        if "records" not in market_data or len(market_data["records"]) == 0:
            return "Unknown", "Unknown", "Not Available"

        record = market_data["records"][0]

        market = record.get("market", "Unknown")
        state = record.get("state", "Unknown")
        price = record.get("modal_price", "Not Available")

        return market, state, price

    except Exception as e:
        print("Market API Error:", e)
        return "Unknown", "Unknown", "Not Available"

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
) 

def ask_ai(user_msg,
           weather_data=None,
           crops=None):

    context = ""

    if weather_data:
        temp, humidity, city = weather_data

        if city:
            context += f"""
City: {city}
Temperature: {temp}°C
Humidity: {humidity}%

Recommended Crops:
{', '.join(crops)}
"""

    prompt = f"""
You are AgroGuideAI,
an intelligent farming assistant.

Rules:
- Reply only in English
- Keep answer short and practical
- Use weather if available
- Answer farming related questions only

Context:
{context}

Farmer Question:
{user_msg}
"""

    models = [

        "openai/gpt-oss-20b:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b:free",
        "google/gemma-4-31b-it:free"

    ]

    for model_name in models:

        try:

            response = (
                client.chat.completions.create(

                    model=model_name,

                    messages=[
                        {
                            "role": "system",
                            "content":
                            "You are a smart farming expert."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.3,
                    max_tokens=180
                )
            )

            return (
                response
                .choices[0]
                .message.content
            )

        except Exception as e:

            print(
                f"{model_name} failed:",
                e
            )

            continue

    return (
        "AI assistant is busy right now. "
        "Please try again in a few seconds."
    )