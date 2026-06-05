import secrets


def generate_webhook_secret() -> str:
    """
    Generate a webhook signing secret.

    Example:
        whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
    return f"whsec_{secrets.token_urlsafe(32)}"
