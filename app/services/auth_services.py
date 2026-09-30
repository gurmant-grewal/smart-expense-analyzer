from app.models import User
from app.security.password_security import hash_password, verify_password
from sqlalchemy.orm import Session
from logging_config import logger
from app.repositories.user_repository import UserRepository
from app.security.auth import create_access_token  


def registration(username:str, password:str, db: Session):
    
    existing_user = UserRepository.get_user_by_username(db, username)
    if existing_user:
        logger.warning("Registration attempt failed: Username already exists - %s", username)
        raise ValueError("username already exists")
    else:
        UserRepository.create_user(db,username,password)
        logger.info("User registered: %s", username)
        return {"message": "User registered successfully."}
    
    
def login(username:str, password:str, db:Session):
    user = UserRepository.get_user_by_username(db, username)
    
    if not user:
        logger.warning("Login attempt failed: User not found - %s", username)
        raise ValueError("User not found.")
    
    
    is_valid_password= verify_password(password, user.password)

    if is_valid_password:
        logger.info("User logged in: %s", username)
        
        token = create_access_token(data={"sub": user.username})

        return {"access_token": token, "token_type": "bearer"}
    
    else:
        logger.warning("Login attempt failed: Invalid password - %s", username)
        raise ValueError("Invalid password.")
       
        
    
