from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form

# Импорт сервисных функций для предсказаний и баланса
from models.crud.prediction_task import create as create_prediction_task, \
    get_by_user_id as get_prediction_tasks_by_user
from models.crud.prediction_result import create as create_prediction_result
from models.crud.balance import get_by_user_id as get_balance, create as create_balance, update_balance
from models.crud.user import get_by_email
from auth.auth import authenticate_cookie
from fastapi.templating import Jinja2Templates

# Зависимость для получения сессии базы данных
from database.database import get_session

from models.PredictionRpcClient import PredictionRpcClient

router = APIRouter()
templates = Jinja2Templates(directory="view")


@router.post("/")
async def predict(request: Request, budget_amount: float = Form(...), preferences:  str   = Form(...), session: Session = Depends(get_session),
                  user:str=Depends(authenticate_cookie)) -> dict:
    """
    Назначает задачу на предсказание для пользователя.
    За каждое предсказание списывается 50 баллов с баланса.
    Создает задачу и симулирует результат предсказания.
    """
    context = {
        "user": user,
        "request": request
    }
    user_id = get_by_email(session, user).id
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
        balance = update_balance(session, balance)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Формируем payload для RPC-запроса
    payload = {
        "user_id": user_id,
        "budget_amount": budget_amount,
        "preferences": preferences
    }
    print('rpc create')
    rpc_client = PredictionRpcClient()
    result = rpc_client.call(payload)

    # Создаем задачу предсказания
    # task = create_prediction_task(session, user_id, budget_amount, preferences)

    # Симулируем алгоритм предсказания: создаем фиктивный результат (например, простую строку)
    # dummy_result = f"{{'predicted': 'dummy result for budget {budget_amount}'}}"
    # result = create_prediction_result(session, task.id, dummy_result)
    print('sesson coomit')
    # session.commit()

    return templates.TemplateResponse(
        "model.html",
        {
            "request": request,
            "user": user,
            "result": result,
            "new_balance": balance.amount
        }
    )


@router.get("/")
async def prediction_history(request: Request, session: Session = Depends(get_session),
                  user:str=Depends(authenticate_cookie)) -> dict:
    """
    Возвращает историю предсказаний для указанного пользователя.
    """
    context = {
        "user": user,
        "request": request
    }
    user_id = get_by_email(session, user).id
    tasks = get_prediction_tasks_by_user(session, user_id)
    return templates.TemplateResponse(
        "model.html",
        {
            "request": request,
            "user": user,
            "prediction_history": tasks
        }
    )
