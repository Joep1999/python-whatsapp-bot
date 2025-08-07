# Simple in-memory session store
user_sessions = {}

def get_user_state(wa_id):
    return user_sessions.get(wa_id, {}).get("state", "NEW")

def set_user_state(wa_id, state):
    if wa_id not in user_sessions:
        user_sessions[wa_id] = {}
    user_sessions[wa_id]["state"] = state

def clear_user_state(wa_id):
    if wa_id in user_sessions:
        user_sessions[wa_id]["state"] = "NEW"
