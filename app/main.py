from database.database import get_settings
from database.database import init_db

if __name__ == "__main__":

    settings = get_settings()
    init_db()
    print('init db success')


