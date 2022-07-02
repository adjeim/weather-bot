import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
WEATHERSTACK_API_KEY = os.environ.get('WEATHERSTACK_API_KEY')

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def weather():
    # Get the user's location from the incoming message
    location = request.values.get('Body', '')

    resp = MessagingResponse()
    msg = resp.message()

    # https://weatherstack.com/documentation
    # Change 'units' to 'm' for metric units
    params = {
        'access_key': WEATHERSTACK_API_KEY,
        'query': location,
        'units': 'f',
    }

    api_result = requests.get('http://api.weatherstack.com/current', params)

    if api_result.status_code == 200:
        data = api_result.json()

        if data.get('error'):
            msg.body('Sorry, I am unable to get weather data for that location.')
        else:
            weather_location = data['location']['name']
            temperature = data['current']['temperature']
            description = data['current']['weather_descriptions'][0]
            precipitation = data['current']['precip']
            uv_index = data['current']['uv_index']

            formatted_response = f'{weather_location}: {temperature}°, {description}. '

            if precipitation > 0:
                formatted_response += 'Bring an umbrella! ☂️ '

            if temperature < 45:
                formatted_response += 'Wear a coat! 🧥 '

            if uv_index > 45:
                formatted_response += 'Wear some sunscreen! ☀️ '

            msg.body(formatted_response)

    else:
        msg.body('Sorry, I am unable to get weather data for that location.')

    return str(resp)

if __name__ == '__main__':
    app.run()