from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_start_battle():
    """
    Проверка на создание битвы.
    """
    response = client.post(
        "/battle/start",
        json=[{"name": "Warrior", "power": 50}, {"name": "Mage", "power": 30}],
    )
    assert response.status_code == 200
    assert "battle_id" in response.json()


def test_get_battle():
    """
    Создание битвы + проверка получения битвы по ID
    """
    response = client.post(
        "/battle/start",
        json=[{"name": "Warrior", "power": 50}, {"name": "Mage", "power": 30}],
    )
    battle_id = response.json()["battle_id"]

    response = client.get(f"/battle/{battle_id}")
    assert response.status_code == 200
    assert response.json()["battle_id"] == battle_id
    assert "winner" in response.json()
    assert response.json()["winner"] in ["Warrior", "Mage"]
