import logging
from flask import current_app, jsonify
import json
import requests

# from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def generate_response(response):
    # Return text in uppercase
    return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


# def process_whatsapp_message(body):
#     wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
#     name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

#     message = body["entry"][0]["changes"][0]["value"]["messages"][0]
#     message_body = message["text"]["body"]

#     # TODO: implement custom function here
#     response = generate_response(message_body)

#     # OpenAI Integration
#     # response = generate_response(message_body, wa_id, name)
#     # response = process_text_for_whatsapp(response)

#     data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
#     send_message(data)

def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_type = message.get("type")

    if message_type == "text":
        # User sent a normal message – send greeting and menu
        greeting_text = (
            f"Hello {name}, I am the Uliza-WI chatbot. I can give you advice on weather-dependent farming practices.\n"
            "How may I assist you?"
        )
        greeting_data = get_text_message_input(wa_id, greeting_text)
        send_message(greeting_data)

        menu_data = get_interactive_menu_input(wa_id)
        send_message(menu_data)

    elif message_type == "interactive":
        interactive_type = message["interactive"]["type"]
        if interactive_type == "button_reply":
            button_id = message["interactive"]["button_reply"]["id"]

            if button_id == "weather_forecast":
                reply_text = "Please share your location or let me know your region so I can fetch the weather forecast for you."

            elif button_id == "farming_advice":
                reply_text = "Please tell me your crop and current situation so I can give tailored farming advice."

            else:
                reply_text = "Sorry, I didn’t understand that option. Please try again."

            data = get_text_message_input(wa_id, reply_text)
            send_message(data)

        else:
            # Future-proof: other interactive types like list_reply
            unknown_text = "Sorry, I couldn't process your selection."
            data = get_text_message_input(wa_id, unknown_text)
            send_message(data)

    else:
        # Unsupported message types like images, voice, etc.
        error_text = "Sorry, I can only understand text and menu selections for now."
        data = get_text_message_input(wa_id, error_text)
        send_message(data)

def get_interactive_menu_input(recipient):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "Please choose an option:"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "weather_forecast",
                                "title": "🌤️ Weather Forecast"
                            },
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "farming_advice",
                                "title": "🌱 Farming Advice"
                            },
                        },
                    ]
                },
            },
        }
    )


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
