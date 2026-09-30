from sqlalchemy.orm import Session
import pandas as pd
from app.repositories.user_repository import UserRepository
from app.repositories.expense_repository import ExpenseRepository
from logging_config import logger


class AnalyticsService:

    @staticmethod
    def get_analytics(db: Session, username: str):

        current_user = UserRepository.get_user_by_username(
            db,
            username
        )

        if not current_user:
            logger.warning("User not found: %s",username)
            raise ValueError("User not found")
        

        df = pd.DataFrame(
        [

        {
            "category": e.category,

            "merchant": e.merchant,

            "amount": e.amount,

            "date": e.date
        }

        for e in ExpenseRepository.get_expense_by_user(db, current_user.id)
        ]
        )

        if df.empty:
            return {
                "top_categories": [],
                "top_merchants": [],
                "largest_merchant": None,
                "daily_expenses": [],
                "category_totals": []
            }

        top_categories = (
            df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5).reset_index()
        )

        merchant_data = ExpenseRepository.get_users_merchant_data(db, current_user.id)

        merchant_df = pd.DataFrame(
            merchant_data,
            columns=["merchant", "total_amount"]
        )

        largest = None

        if not merchant_df.empty:
            largest = merchant_df.loc[
                merchant_df["total_amount"].idxmax()
            ].to_dict()

        return {

            "top_categories": top_categories.to_dict("records"),

            "top_merchants": merchant_df.to_dict("records"),

            "largest_merchant": largest,

            "category_totals": (
                df.groupby("category")["amount"]
                .sum()
                .to_dict()
            ),

            "daily_expenses": (
                df.groupby("date")["amount"]
                .sum()
                .to_dict()
            )
        }
    @staticmethod

    def get_spending_insights(

        db: Session,
        username: str
    ):

        current_user = UserRepository.get_user_by_username(
            db,
            username
        )

        if current_user is None:
            logger.exception("user not found for getting spending insights")
            raise ValueError("User not found.")
        

        df = pd.DataFrame([

        {
        "category": e.category,
        "amount": e.amount,
        "date": e.date
        }

        for e in ExpenseRepository.get_expense_by_user(db,current_user.id)
        ])

        if df.empty:
            return []

        df["date"] = pd.to_datetime(df["date"])

        latest_day = df["date"].max()

        previous_day = latest_day - pd.Timedelta(days=1)

        latest_df = df[df["date"] == latest_day]

        previous_df = df[df["date"] == previous_day]

        insights = []

        for category in sorted(df["category"].unique()):

            latest_total = (
                latest_df[
                    latest_df["category"] == category
                ]["amount"].sum()
            )

            previous_total = (
                previous_df[
                    previous_df["category"] == category
                ]["amount"].sum()
            )

            if previous_total == 0:

                insights.append({
                    "category": category,
                    "status": "no_previous_data",
                    "current_amount": float(latest_total),
                    "previous_amount": 0,
                    "difference": float(latest_total),
                    "percentage_change": None
                })

                continue

            difference = latest_total - previous_total

            percentage = (
                difference / previous_total
            ) * 100

            if difference > 0:
                status = "increase"

            elif difference < 0:
                status = "decrease"

            else:
                status = "unchanged"

            insights.append({
                "category": category,
                "status": status,
                "current_amount": float(latest_total),
                "previous_amount": float(previous_total),
                "difference": float(difference),
                "percentage_change": round(
                    percentage,
                    2
                )
            })

        return insights