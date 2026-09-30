from sqlalchemy.orm import Session
from app.models import User
from app.security.password_security import hash_password, verify_password

class UserRepository:
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def create_user(db: Session, username: str, password: str):
        new_user = User(username=username, password=hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    