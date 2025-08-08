from app.session.session_store import set_user_state, clear_user_state


def handle_weather_request(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]

    # Ask for location
    text = "Please tell me your location 🌍 so I can check the forecast."
    data = get_text_message_input(wa_id, text)
    send_message(data)

    # Update user state
    set_user_state(wa_id, "AWAITING_WEATHER_LOCATION")

def handle_location_input(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]
    location = message["text"]["body"]

    reply = f"Got it! Checking weather for *{location}*... ☁️"
    data = get_text_message_input(wa_id, reply)
    send_message(data)

    # Call weather API here...

    clear_user_state(wa_id)