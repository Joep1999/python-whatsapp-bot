from app.session.session_store import set_user_state, clear_user_state

def handle_unknown(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message["from"]

    # Ask for crop
    text = "Sorry but I cannot handle this input."
    data = get_text_message_input(wa_id, text)
    send_message(data)

    # Clear user state
    clear_user_state(wa_id)