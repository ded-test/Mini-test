from fastapi import FastAPI, HTTPException
import random
from models import Participant, Battle
import uvicorn

app = FastAPI()

# Вместо реальной БД
battles = {}
battle_id_counter = 1

@app.post("/battle/start")
def start_battle(participants: list[Participant]):
    """
    Принимает JSON с двумя участниками и
    их характеристиками (например, name и power),
    возвращает ID битвы
    """

    if len(participants) != 2:
        raise HTTPException(status_code=400, detail="Должно быть ровно 2 участника!")

    global battle_id_counter
    battle_id = battle_id_counter
    battles[battle_id] = Battle(id=battle_id, participants=participants)
    battle_id_counter += 1
    return {"battle_id": battle_id}

@app.get("/battle/{id}")
def get_battle(id: int):
    """
    Возвращает результат битвы, где победитель
    определяется случайно с учетом поля power
    """
    if id not in battles:
        raise HTTPException(status_code=404, detail="Битва не найдена!")

    battle = battles[id]

    # Пустой список в котором каждый участник будет
    # повторяться в зависимости от своей силы.
    weighted_participants = []
    for participant in battle.participants:
        weighted_participants.extend([participant] * participant.power)

    winner = random.choice(weighted_participants)

    battle.winner = winner.name

    return {
        "battle_id": battle.id,
        "participants": battle.participants,
        "winner": battle.winner
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)