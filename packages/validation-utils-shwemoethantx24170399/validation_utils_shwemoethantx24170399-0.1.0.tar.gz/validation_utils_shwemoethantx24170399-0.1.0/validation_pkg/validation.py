def check_battery_level(battery_level):
    """Validate battery level is between 0 and 100."""
    return 0 <= battery_level <= 100

def check_user_role(user, role='admin'):
    """Check if a user has a specific role (e.g., 'admin')."""
    if user is None:
        return False
    if role == 'admin':
        return hasattr(user, 'is_staff') and user.is_staff
    return False