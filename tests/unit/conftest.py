import pytest

from app.services import demo_service


@pytest.fixture(autouse=True)
def set_test_pickle_file_location(monkeypatch):
    """
    Override file path, to load `test_data.pkl` file instead.
    """
    monkeypatch.setattr(demo_service, "PICKLE_FILENAME", "test_data.pkl")
