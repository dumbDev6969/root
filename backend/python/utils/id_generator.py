import uuid
import time
from typing import Optional

def generate_user_id(prefix: str = "USR") -> str:
    """
    Generate a unique user ID with timestamp and UUID.
    
    Args:
        prefix (str): Optional prefix for the user ID. Defaults to "USR".
    
    Returns:
        str: A unique user ID in format: {prefix}{timestamp_short}{uuid_short}
    """
    try:
        # Get current timestamp and take last 6 digits
        timestamp = str(int(time.time()))[-6:]
        # Generate UUID and take first 8 characters
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        # Combine components without underscores to save space
        user_id = f"{prefix}{timestamp}{unique_id}"
        return user_id
    except Exception as e:
        print(f"Error generating user ID: {e}")
        # Fallback to simple UUID if timestamp fails
        return f"{prefix}{str(uuid.uuid4())[:12]}"

def is_valid_user_id(user_id: str) -> bool:
    """
    Validate if a string matches the expected user ID format.
    
    Args:
        user_id (str): The user ID to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if len(user_id) != 17:  # 3 char prefix + 6 char timestamp + 8 char uuid
            return False
            
        prefix = user_id[:3]
        timestamp = user_id[3:9]
        uuid_part = user_id[9:]
        
        # Validate prefix
        if not prefix.isalpha():
            return False
            
        # Validate timestamp
        if not timestamp.isdigit():
            return False
            
        # Validate UUID part (should be 8 characters of hex digits)
        if len(uuid_part) != 8 or not all(c in '0123456789abcdef' for c in uuid_part.lower()):
            return False
            
        return True
    except:
        return False

# Example usage
if __name__ == "__main__":
    # Generate a user ID
    user_id = generate_user_id()
    print(f"Generated User ID: {user_id}")
    
    # Validate the generated ID
    is_valid = is_valid_user_id(user_id)
    print(f"Is Valid: {is_valid}")
    
    # Example with custom prefix
    custom_id = generate_user_id(prefix="EMP")
    print(f"Custom Prefix ID: {custom_id}")