from .config import load_api_key, save_api_key, check_first_time_setup
from .gemini_api import init_gemini, get_command

# Initialize Gemini globally
def initialize_gemini():
    """Initialize Gemini with the saved API key."""
    if not check_first_time_setup():
        return None

    api_key = load_api_key()
    if not api_key:
        print("❌ No API key found. Exiting...")
        return None

    init_gemini(api_key)
    return api_key
