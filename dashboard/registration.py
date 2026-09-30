import streamlit as st
from sqlalchemy import func
from database import SessionLocal,get_session
from app.services.auth_services import registration




def register_user(username, password):
    with get_session() as db:

        registration(
            username=username,
            password=password,
            db=db
        )

    st.success(
        "Registration successful."
    )
    