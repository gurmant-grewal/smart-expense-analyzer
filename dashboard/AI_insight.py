import streamlit as st

from database import get_session
from app.services.analytics import AnalyticsService


def show_ai_insights():

    try:
        with get_session() as db:
            insights = (
                AnalyticsService
                .get_spending_insights(
                    db,
                    st.session_state.username
                )
            )

        st.subheader("Spending Insights")

        if not insights:
            st.info("No expense data available.")
            return

        for insight in insights:
            category = insight["category"]
            if insight["status"] == "increase":
                st.warning(
                    f"{category} spending increased by "
                    f"${insight['difference']:.2f} "
                    f"({insight['percentage_change']}%)"
                )

            elif insight["status"] == "decrease":
                st.success(
                    f"{category} spending decreased by "
                    f"${abs(insight['difference']):.2f} "
                    f"({abs(insight['percentage_change'])}%)"
                )

            elif insight["status"] == "unchanged":
                st.info(
                    f"{category} spending remained unchanged."
                )

            else:
                st.info(
                    f"No previous spending data for {category}."
                )

    except Exception as e:

        st.error(str(e))