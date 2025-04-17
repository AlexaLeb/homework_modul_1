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


