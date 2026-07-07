# promote.py
from database import SessionLocal
import models

db = SessionLocal()
user_email = str(input("Enter the email of the user to promote to Admin: "))
user = db.query(models.User).filter(models.User.email == user_email).first()
if user:
    user.role = "admin"
    db.commit()
    print(f"✅ User {user.email} promoted to Admin!")
else:
    print("❌ User not found.")
db.close()