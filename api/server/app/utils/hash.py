
#create a function that hashes a password using MD5
import hashlib
import hmac

async def hash_password(password: str) -> str:
    hash_pass = hashlib.md5(password.encode())
    return hash_pass.hexdigest()

async def hmac_sha256(data, secret):
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
