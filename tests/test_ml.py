from app.services.ml_services import predict_category
from app.utils import clean_text
from app.utils import extract_merchant

def test_prediction_returns_tuple():

    result = predict_category(
        "Pizza from Dominos"
    )

    assert isinstance(result, tuple)

def test_prediction_returns_string():

    category, confidence = predict_category(
        "Pizza"
    )

    assert isinstance(category, str)

def test_prediction_confidence():

    category, confidence = predict_category(
        "Pizza"
    )

    assert 0 <= confidence <= 1

def test_prediction_not_empty():

    category, confidence = predict_category(
        "Pizza"
    )

    assert category != ""

def test_empty_prediction():

    category, confidence = predict_category(
        ""
    )

    assert category == "Unknown"

    assert confidence == 0.0

def test_extract_merchant():

    merchant = extract_merchant(
        "Ordered Pizza from Dominos"
    )

    assert merchant == "dominos"

def test_extract_unknown_merchant():

    merchant = extract_merchant(
        "Local grocery store"
    )

    assert merchant is None

def test_clean_text():

    text = clean_text(
        "Hello!!! 123 World"
    )

    assert text == "hello world"

def test_clean_spaces():

    text = clean_text(
        "    Pizza      From      Dominos    "
    )

    assert text == "pizza from dominos"

def test_confidence_is_float():

    category, confidence = predict_category(
        "Netflix Subscription"
    )

    assert isinstance(confidence, float)

