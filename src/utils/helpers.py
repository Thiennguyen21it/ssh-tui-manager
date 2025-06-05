import os
import re
from typing import Optional, Tuple

def validate_hostname(hostname: str) -> Tuple[bool, str]:
    """Validate a hostname or IP address."""
    # Simple hostname validation
    if not hostname or len(hostname) > 255:
        return False, "Hostname must be between 1 and 255 characters"
    
    # Check if it's an IP address
    ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    if re.match(ip_pattern, hostname):
        # Validate each octet
        octets = hostname.split(".")
        for octet in octets:
            if not 0 <= int(octet) <= 255:
                return False, "IP address octets must be between 0 and 255"
        return True, ""
    
    # Check hostname format
    hostname_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
    if not re.match(hostname_pattern, hostname):
        return False, "Invalid hostname format"
    
    return True, ""

def validate_port(port: str) -> Tuple[bool, str]:
    """Validate a port number."""
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return True, ""
        return False, "Port must be between 1 and 65535"
    except ValueError:
        return False, "Port must be a number"

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate a username."""
    if not username:
        return False, "Username cannot be empty"
    
    # Simple username validation
    username_pattern = r"^[a-zA-Z0-9_\-\.]+$"
    if not re.match(username_pattern, username):
        return False, "Username contains invalid characters"
    
    return True, ""

def validate_key_path(path: Optional[str]) -> Tuple[bool, str]:
    """Validate an SSH key file path."""
    if not path:
        return True, ""  # Empty path is valid (will use password auth)
    
    if not os.path.exists(path):
        return False, "Key file does not exist"
    
    if not os.path.isfile(path):
        return False, "Path is not a file"
    
    return True, ""

def expand_path(path: str) -> str:
    """Expand user path (e.g., ~/keys/id_rsa to /home/user/keys/id_rsa)."""
    return os.path.expanduser(path) 