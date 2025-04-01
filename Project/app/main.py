from Project.app.database.database import get_session
from database.database import engine
from database.database import get_settings
from database.database import init_db
from sqlmodel import Session
from models.crud.user import create_user, get_all_users, get_by_email
import models.crud.transaction as tr
import models.crud.balance as balance
from models.Balance import Balance

if __name__ == "__main__":

    settings = get_settings()
    print(settings.DB_HOST)
    print(settings.DB_NAME)

    init_db()
    print('init db success')

    session = next(get_session())
    create_user(session, "test1", "12", False)
    balance.create(session, user_id=get_by_email(session, 'test1').id, initial_amount=100.0)
    create_user(session, 'test2', "13", False)
    balance.create(session, user_id=get_by_email(session, 'test2').id, initial_amount=80.0)
    users = get_all_users(session)

    for user in users:
        print(f'\nid {user.id} - {user.username}')
        print(f'pw {user.check_password("12")}')
        print(user)

    # Получаем демо-пользователя по имени
    demo_user = get_by_email(session, "test1")
    if not demo_user:
        print("Демо-пользователь не найден. Запустите init_db.py для инициализации базы.")
    else:
        print(f'\n demo user - {demo_user}')

        # Пополнение баланса
    tr.create(session, user_id=demo_user.id, transaction_type="deposit", amount=25)
    demo_user.balance.deposit(25)
    session.commit()
    print(f"\nПосле пополнения баланс: {demo_user.balance.amount}")

    try:
        tr.create(session, user_id=demo_user.id, transaction_type="withdrawal", amount=40)
        demo_user.balance.withdraw(40)
        session.commit()
        print(f"\nПосле списания баланс: {demo_user.balance.get_amount()}")
    except Exception as e:
        print("\nОшибка при списании средств:", e)

    print("\nИстория транзакций:")
    transactions = tr.get_by_user_id(session, demo_user.id)
    for tx in transactions:
        print(f"{tx.transaction_type} - {tx.amount} ({tx.timestamp})")

    session.close()
