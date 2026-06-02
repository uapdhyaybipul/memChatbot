import bcrypt

def hash_password(plain_password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Convert back to a UTF-8 string for database storage
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored bcrypt hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Check if the passwords match
    return bcrypt.checkpw(password_bytes, hashed_bytes)
