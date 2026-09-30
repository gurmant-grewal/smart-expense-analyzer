from app.services import auth_services
from database import get_session
import streamlit as st



def show_login(username, password):
    with get_session() as db:

        user = auth_services.login(
            db=db,
            username=username,
            password=password
        )
 
    if user:
        st.session_state.logged_in = True
       

    st.session_state.username = username