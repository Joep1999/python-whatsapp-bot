import json

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