from app.main import app


def test_main_exposes_routes():
    assert app
    assert len(app.routes) == 7
