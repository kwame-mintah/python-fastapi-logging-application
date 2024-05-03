import os.path

import pytest

from app.services import demo_service


@pytest.fixture(autouse=True)
def set_test_pickle_file_location(monkeypatch):
    """
    Override file path, to load `test_data.pkl` file instead.
    """
    directory_path = os.path.dirname(os.path.realpath(__file__))
    monkeypatch.setattr(
        demo_service, "PICKLE_FILENAME", os.path.join(directory_path, "test_data.pkl")
    )
