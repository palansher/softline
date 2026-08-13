from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_calculate_api_success() -> None:
    """Тест успешного запроса к API."""
    response = client.post("/api/calculate", json={"expression": "10 + 5 * 2"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "result": 20}


def test_calculate_api_division_by_zero() -> None:
    """Тест ошибки деления на ноль через API."""
    response = client.post("/api/calculate", json={"expression": "10 / 0"})
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "Деление на 0!"}


def test_calculate_api_invalid_payload() -> None:
    """Тест автоматической валидации Pydantic (неверный формат тела)."""
    response = client.post("/api/calculate", json={"invalid_field": "123"})
    assert response.status_code == 422  # Unprocessable Entity от Pydantic
