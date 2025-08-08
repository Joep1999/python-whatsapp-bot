from app.modules.start.handlers.main_menu import get_interactive_menu_input
from app.session.session_store import set_user_state

def handle_first_message(message):
    from app.utils.whatsapp_utils import get_text_message_input, send_message
    wa_id = message['from']
    user_name = message['user_name']

    greeting_text = (
            f"Hello {user_name}, I am the Uliza-WI chatbot. I can give you advice on weather-dependent farming practices.\n"
            "How may I assist you?"
        )
    data = get_text_message_input(wa_id, greeting_text)
    send_message(data)

    menu_data = get_interactive_menu_input(wa_id)
    send_message(menu_data)

    set_user_state(wa_id, "IDLE")