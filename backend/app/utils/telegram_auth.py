"""
Telegram Web App authentication utilities.
Validates initData from Telegram Web App and extracts user information.
"""

import hmac
import hashlib
import json
from urllib.parse import parse_qs, unquote
from typing import Dict, Optional
from app.config import settings


def validate_telegram_init_data(init_data: str) -> bool:
    """
    Validate Telegram Web App initData.

    Args:
        init_data: The initData string from Telegram Web App

    Returns:
        True if valid, False otherwise

    Reference:
        https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        # Parse init_data
        parsed = parse_qs(init_data)

        # Extract hash
        received_hash = parsed.get('hash', [None])[0]
        if not received_hash:
            return False

        # Remove hash from data
        data_check_string_parts = []
        for key in sorted(parsed.keys()):
            if key == 'hash':
                continue
            value = parsed[key][0]
            data_check_string_parts.append(f"{key}={value}")

        data_check_string = '\n'.join(data_check_string_parts)

        # Create secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=settings.telegram_bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Compare hashes
        return hmac.compare_digest(received_hash, calculated_hash)

    except Exception as e:
        print(f"Error validating Telegram initData: {e}")
        return False


def extract_user_from_init_data(init_data: str) -> Optional[Dict]:
    """
    Extract user information from Telegram Web App initData.

    Args:
        init_data: The initData string from Telegram Web App

    Returns:
        Dictionary with user info (id, first_name, last_name, username) or None
    """
    try:
        parsed = parse_qs(init_data)
        user_json = parsed.get('user', [None])[0]

        if not user_json:
            return None

        # Decode and parse JSON
        user_data = json.loads(unquote(user_json))

        return {
            'telegram_id': user_data.get('id'),
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'username': user_data.get('username'),
            'language_code': user_data.get('language_code', 'it'),
        }

    except Exception as e:
        print(f"Error extracting user from initData: {e}")
        return None


def get_user_display_name(user_info: Dict) -> str:
    """
    Get a display name from user info.

    Args:
        user_info: User info dictionary from extract_user_from_init_data

    Returns:
        Display name (first_name + last_name or username)
    """
    first_name = user_info.get('first_name', '')
    last_name = user_info.get('last_name', '')
    username = user_info.get('username', '')

    if first_name:
        full_name = f"{first_name} {last_name}".strip()
        return full_name if full_name else username or "User"

    return username or "User"
