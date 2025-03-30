from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_session
from models.crud.balance import get_by_user_id as get_balance, create as create_balance
from models.crud.transaction import create as create_transaction

router = APIRouter()


@router.get("/balance")
async def read_balance(user_id: int, session: Session = Depends(get_session)) -> dict:
    """
    Возвращает текущий баланс пользователя по его user_id.
    """
    balance = get_balance(session, user_id)
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Balance not found for the given user_id"
        )
    return {"user_id": user_id, "balance": balance.amount}


@router.post("/balance/deposit")
async def deposit_balance(user_id: int, amount: float, session: Session = Depends(get_session)) -> dict:
    """
    Пополнение баланса пользователя.
    Если баланс отсутствует, создаёт новый с начальным значением 0.0.
    После пополнения автоматически создаётся транзакция с типом 'deposit'.
    """
    balance = get_balance(session, user_id)
    if not balance:
        balance = create_balance(session, user_id, initial_amount=0.0)

    try:
        balance.deposit(amount)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Записываем транзакцию пополнения
    create_transaction(session, user_id, "deposit", amount)

    session.commit()
    session.refresh(balance)
    return {"user_id": user_id, "new_balance": balance.amount}
