import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from database import get_session
from app.services.analytics import AnalyticsService


def show_analytics():

    with get_session() as db:

        analytics = AnalyticsService.get_analytics(
            db,
            st.session_state.username
        )

    st.subheader("Top Spending Categories")

    st.dataframe(
        pd.DataFrame(
            analytics["top_categories"]
        ),
        use_container_width=True
    )

    st.subheader("Top Merchants")

    st.dataframe(
        pd.DataFrame(
            analytics["top_merchants"]
        )
    )

    if analytics["largest_merchant"]:

        merchant = analytics["largest_merchant"]

        st.metric(
            "Biggest Merchant",
            merchant["merchant"],
            f"${merchant['total_amount']:.2f}"
        )

    fig, ax = plt.subplots()

    ax.bar(
        analytics["category_totals"].keys(),
        analytics["category_totals"].values()
    )

    st.pyplot(fig)

    fig2, ax2 = plt.subplots()

    ax2.bar(
        analytics["daily_expenses"].keys(),
        analytics["daily_expenses"].values()
    )

    st.pyplot(fig2)