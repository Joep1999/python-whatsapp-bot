from app.session.session_store import set_user_state, clear_user_state
from app.utils.text_utils import remove_emojis


def handle_weather_request(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message, get_location_request, send_tts_message
    wa_id = message["from"]

    # Ask for location
    reply = "Please share with me your location 🌍 so I can check the forecast."
    location_request_data = get_location_request(wa_id, reply)
    send_message(location_request_data)

    # Send voice message
    send_tts_message(wa_id ,remove_emojis(reply))

    # Update user state
    set_user_state(wa_id, "AWAITING_WEATHER_LOCATION")

def handle_location_input(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message, send_tts_message
    wa_id = message["from"]
    location = message["text"]["body"]

    reply = f"Got it! However, to check the weather for *{location}* you need to share the location using Whatsapp interface!"
    data = get_text_message_input(wa_id, reply)
    send_message(data)
    # Send voice message
    send_tts_message(wa_id ,remove_emojis(reply))

    # Call weather API here...

    clear_user_state(wa_id)

def handle_location_share(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message, send_tts_message
    wa_id = message["from"]
    location = message["location"]
    location_name = location.get("name", "Unknown location")
    location_address = location.get("address", "")

    latitude = location["latitude"]
    longitude = location["longitude"]

    reply = f"📍 Got your location!\nLatitude: {latitude}, Longitude: {longitude}"
    if location_name != "Unknown location":
        reply += f"\nPlace: {location_name}"
    if location_address:
        reply += f"\nAddress: {location_address}"
    reply += "\nChecking weather... ☁️"

    data = get_text_message_input(wa_id, reply)
    send_message(data)

    send_image_message_wrapper(wa_id)

    # Send voice message
    send_tts_message(wa_id ,remove_emojis(reply))

    # Call your weather API here with (latitude, longitude)
    # weather = get_weather_by_coords(latitude, longitude)
    # send_message(get_text_message_input(wa_id, weather))

    clear_user_state(wa_id)