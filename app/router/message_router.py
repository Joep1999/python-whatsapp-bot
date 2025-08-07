from app.modules.fallback import fallback
from app.modules.weather_forecast import weather_forecast
from app.modules.farming_advice import farming_advice
from app.modules.start import start
from app.session.session_store import get_user_state

def route_message(message):
    wa_id = message["from"]
    state = get_user_state(wa_id)

    if state == "NEW":
        return start.handle_first_message(message)
    elif state == "IDLE":
        if message.get("type") == "interactive":
            button_id = message["interactive"]["button_reply"]["id"]
            if button_id == "weather_forecast":
                return weather_forecast.handle_weather_request(message)
            elif button_id == "farming_advice":
                return farming_advice.handle_farming_request(message)

        elif message.get("type") == "text":
            if state == "AWAITING_WEATHER_LOCATION":
                return weather_forecast.handle_location_input(message)
            elif state == "AWAITING_CROP_INFO":
                return farming_advice.handle_crop_input(message)
            else:
                return fallback.handle_unknown(message)
