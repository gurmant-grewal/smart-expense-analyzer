from app.models import Expense
from app.repositories.user_repository import UserRepository
from app.repositories.expense_repository import ExpenseRepository
from app.services.analytics import AnalyticsService


def test_empty_analytics(db):

    UserRepository.create_user(
        db,
        username="analytics",
        password="password123"
    )

    analytics = AnalyticsService.get_analytics(
        db,
        "analytics"
    )

    assert analytics["top_categories"] == []


def test_analytics_returns_categories(db):

    user = UserRepository.create_user(
        db,
        username="john",
        password="password123"
    )

    ExpenseRepository.create_expense(
        db,
        Expense(
            user_id=user.id,
            text="Pizza",
            category="food",
            amount=500,
            merchant="dominos",
            feedback_verified=True,
        )
    )

    analytics = AnalyticsService.get_analytics(
        db,
        "john"
    )

    assert len(
        analytics["top_categories"]
    ) > 0


def test_largest_merchant(db):

    user = UserRepository.create_user(
        db,
        username="merchant",
        password="password123"
    )

    ExpenseRepository.create_expense(
        db,
        Expense(
            user_id=user.id,
            text="Netflix",
            category="entertainment",
            amount=900,
            merchant="netflix",
            feedback_verified=True,
        )
    )

    analytics = AnalyticsService.get_analytics(
        db,
        "merchant"
    )

    assert analytics["largest_merchant"] is not None


def test_spending_insights_returns_list(db):

    user = UserRepository.create_user(
        db,
        username="insight",
        password="password123"
    )

    ExpenseRepository.create_expense(
        db,
        Expense(
            user_id=user.id,
            text="Pizza",
            category="food",
            amount=500,
            feedback_verified=True,
        )
    )

    insights = AnalyticsService.get_spending_insights(
        db,
        "insight"
    )

    assert isinstance(
        insights,
        list
    )