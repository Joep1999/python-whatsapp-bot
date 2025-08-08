from app.session.session_store import set_user_state, clear_user_state

def handle_farming_request(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]

    # Ask for crop
    text = "Tell me what you’re growing 🌾 and I’ll give you some advice."
    data = get_text_message_input(wa_id, text)
    send_message(data)

    # Update user state
    set_user_state(wa_id, "AWAITING_CROP_INFO")


def handle_crop_input(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]
    crop = message["text"]["body"]

    reply = f"Got it! Checking farming advice for *{crop}*... 🌾"
    data = get_text_message_input(wa_id, reply)
    send_message(data)

    # Call weather API here...

    clear_user_state(wa_id)
