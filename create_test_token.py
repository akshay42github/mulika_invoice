from jose import jwt 
from datetime import datetime, timedelta

SECRET_KEY = "mulika-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"

payload = {
    "sub": "dev1@mulika.com",
    "organization_id": "00000000-0000-0000-0000-000000000001",
    "role": "admin",
    "exp": datetime.utcnow() + timedelta(minutes=24)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print("Your test Token:")
print(token)