from app.session.session_store import set_user_state, clear_user_state


def handle_weather_request(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message, get_location_request
    wa_id = message["from"]

    # Ask for location
    text = "Please share with me your location 🌍 so I can check the forecast."
    location_request_data = get_location_request(wa_id, text)
    send_message(location_request_data)

    # Update user state
    set_user_state(wa_id, "AWAITING_WEATHER_LOCATION")

def handle_location_input(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]
    location = message["text"]["body"]

    reply = f"Got it! However, to check the weather for *{location}* you need to share the location using Whatsapp interface!"
    data = get_text_message_input(wa_id, reply)
    send_message(data)

    # Call weather API here...

    clear_user_state(wa_id)

def handle_location_share(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]
    location = message["location"]
    location_name = location["name"]
    location_address = location["address"]

    latitude = location["latitude"]
    longitude = location["longitude"]

    reply = f"📍 Got your location!\nLatitude: {latitude}, Longitude: {longitude}\nName: {location_name}\nAddress: {location_address}\nChecking weather... ☁️"
    data = get_text_message_input(wa_id, reply)
    send_message(data)

    # Call your weather API here with (latitude, longitude)
    # weather = get_weather_by_coords(latitude, longitude)
    # send_message(get_text_message_input(wa_id, weather))

    clear_user_state(wa_id)