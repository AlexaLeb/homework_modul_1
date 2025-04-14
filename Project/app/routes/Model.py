from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Импорт сервисных функций для предсказаний и баланса
from models.crud.prediction_task import create as create_prediction_task, \
    get_by_user_id as get_prediction_tasks_by_user
from models.crud.prediction_result import create as create_prediction_result
from models.crud.balance import get_by_user_id as get_balance, create as create_balance

# Зависимость для получения сессии базы данных
from database.database import get_session

from models.PredictionRpcClient import PredictionRpcClient

router = APIRouter()


@router.post("/predict")
async def predict(user_id: int, budget_amount: float, preferences: str,
                  session: Session = Depends(get_session)) -> dict:
    """
    Назначает задачу на предсказание для пользователя.
    За каждое предсказание списывается 50 баллов с баланса.
    Создает задачу и симулирует результат предсказания.
    """
    # Получаем баланс пользователя; если баланс не существует, создаем его с начальным значением 0.0
    balance = get_balance(session, user_id)
    if not balance:
        balance = create_balance(session, user_id, initial_amount=0.0)

    if balance.amount < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance for prediction (requires at least 50 points)"
        )

    # Списываем 50 баллов с баланса
    try:
        balance.withdraw(50)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Формируем payload для RPC-запроса
    payload = {
        "user_id": user_id,
        "budget_amount": budget_amount,
        "preferences": preferences
    }

    rpc_client = PredictionRpcClient()
    result = rpc_client.call(payload)

    # Создаем задачу предсказания
    task = create_prediction_task(session, user_id, budget_amount, preferences)

    # Симулируем алгоритм предсказания: создаем фиктивный результат (например, простую строку)
    dummy_result = f"{{'predicted': 'dummy result for budget {budget_amount}'}}"
    result = create_prediction_result(session, task.id, dummy_result)

    session.commit()

    return {
        "message": "Prediction task created",
        "task_id": task.id,
        "result": result.recommended_distribution,
        "new_balance": balance.amount
    }


@router.get("/prediction/history")
async def prediction_history(user_id: int, session: Session = Depends(get_session)) -> dict:
    """
    Возвращает историю предсказаний для указанного пользователя.
    """
    tasks = get_prediction_tasks_by_user(session, user_id)
    return {"user_id": user_id, "prediction_history": tasks}
