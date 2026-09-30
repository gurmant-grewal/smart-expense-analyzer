import streamlit as st
from dashboard.login import show_login
from dashboard.registration import registration
from dashboard.add_expense import show_add_expense
from dashboard.analytics import show_analytics
from dashboard.AI_insight import show_ai_insights
from dashboard.ml_model_performance import show_model_performance


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.logged_in:

    menu = st.selectbox(
        "Choose an option",
        ["Login", "Register"]
    )

    if menu == "Login":
        show_login()

    else:
        registration()

else:

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Add Expense",
            "Analytics",
            "AI Insights",
            "Model Performance"
        ]
    )

    if menu == "Add Expense":
        show_add_expense()

    elif menu == "Analytics":
        show_analytics()

    elif menu == "AI Insights":
        show_ai_insights()

    elif menu == "Model Performance":
        show_model_performance()   