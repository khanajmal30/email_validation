import re
from typing import Dict

def validate_email_addr(email_addr: str) -> bool:
    """
    Returns True if the email_addr is valid per specification. Otherwise, returns False.
    """
    # Total length of email too long.
    if len(email_addr) > 254:
        return False

    # Check for exactly one '@' symbol
    if email_addr.count('@') != 1:
        return False

    # Split local and domain parts
    local_part, domain_part = email_addr.split('@')
    
    # Check length of local and domain parts
    if len(local_part) > 64 or len(domain_part) > 251:
        return False

    # Validate characters
    if not re.match(r'^[a-zA-Z0-9._-]+$', local_part):
        return False
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain_part):
        return False

    # Check hyphen and dot positions in local part
    if local_part.startswith(('.', '-')) or local_part.endswith(('.', '-')):
        return False
    
    # Check top-level domain
    if not domain_part.endswith(('.com', '.net', '.org')):
        return False
    
    return True

def validate_email_payload(sender_name: str, sender_addr: str, receiver_name: str, receiver_addr: str, html: str, replacements: Dict) -> bool:
    """
    Returns True if the payload is validated and is safe to send out. Otherwise, returns False.
    """

    # Validate sender name
    if not (5 <= len(sender_name.strip()) <= 30):
        return False

    # Validate receiver name
    if not (5 <= len(receiver_name.strip()) <= 60):
        return False

    # Validate sender email address
    if not validate_email_addr(sender_addr):
        return False

    # Validate receiver email address
    if not validate_email_addr(receiver_addr):
        return False

    # Validate replacements dictionary
    if not replacements:
        return False

    # Ensure non-empty replacement values
    for key, value in replacements.items():
        if not value:
            return False
    
    # Ensure all keys in replacements are used in HTML
    keys_in_html = re.findall(r'\{(.*?)\}', html)
    for key in keys_in_html:
        if key not in replacements:
            return False

    # Ensure there are no surplus placeholders
    for key in replacements:
        if key not in keys_in_html:
            return False
    
    return True


