import streamlit as st
from database import get_session
from app.services.expense_services import (
    analyze_expense,
    add_expense
)

from app.constants import CATEGORIES


def show_add_expense():

    st.subheader("Add Expense")

    with st.form("expense_form"):
        text = st.text_input("Expense")
        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        submitted = st.form_submit_button(
            "Analyze"
        )

    if not submitted:
        return

    analysis = analyze_expense(
        text=text,
        amount=amount
    )

    st.success(
        f"Predicted Category: "
        f"{analysis['category']}"
    )

    accept = st.radio(
        "Is this prediction correct?",
        ["Yes", "No"]
    )

    corrected = None

    if accept == "No":
        corrected = st.selectbox(
            "Correct Category",
            CATEGORIES
        )

    if st.button("Save Expense"):

        with get_session() as db:

            add_expense(
                db=db,
                username=st.session_state.username,
                text=text,
                amount=amount,
                predicted_category=analysis["category"],
                corrected_category=corrected
            )

        st.success(
            "Expense saved successfully."
        )
        