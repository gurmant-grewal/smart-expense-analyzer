from app.models import Expense
from app.repositories.user_repository import UserRepository
from app.repositories.expense_repository import ExpenseRepository


def test_create_user(db):

    user = UserRepository.create_user(
        db,
        username="john",
        password="password123"
    )

    assert user.id is not None
    assert user.username == "john"


def test_get_user_by_username(db):

    UserRepository.create_user(
        db,
        username="alice",
        password="password123"
    )

    user = UserRepository.get_user_by_username(
        db,
        "alice"
    )

    assert user is not None
    assert user.username == "alice"


def test_create_expense(db):

    user = UserRepository.create_user(
        db,
        username="expenseuser",
        password="password123"
    )

    expense = Expense(
        user_id=user.id,
        text="Pizza",
        category="food",
        amount=500,
        merchant="dominos",
        feedback_verified=True,
    )

    ExpenseRepository.create_expense(
        db,
        expense
    )

    assert expense.id is not None


def test_get_expenses_by_user(db):

    user = UserRepository.create_user(
        db,
        username="user1",
        password="password123"
    )

    ExpenseRepository.create_expense(
        db,
        Expense(
            user_id=user.id,
            text="Coffee",
            category="food",
            amount=100,
            feedback_verified=True,
        )
    )

    expenses = ExpenseRepository.get_expense_by_user(
        db,
        user.id
    )

    assert len(expenses) == 1


def test_verified_expense_count(db):

    user = UserRepository.create_user(
        db,
        username="verified",
        password="password123"
    )

    ExpenseRepository.create_expense(
        db,
        Expense(
            user_id=user.id,
            text="Uber",
            category="transportation",
            amount=250,
            feedback_verified=True,
        )
    )

    count = ExpenseRepository.verify_expense_count(db)

    assert count >= 1