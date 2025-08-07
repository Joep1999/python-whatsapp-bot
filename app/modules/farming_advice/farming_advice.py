from app.utils.whatsapp_utils import get_text_message_input, send_message

def handle_farming_request(message):
    wa_id = message["from"]
    text = "Tell me what you’re growing 🌾 and I’ll give you some advice."
    data = get_text_message_input(wa_id, text)
    send_message(data)
