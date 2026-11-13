import os

from dotenv import load_dotenv

from bot import Mapler
from service import DBService

if __name__ == "__main__":
    load_dotenv()

    db = DBService(os.environ.get("DATABASE_URL"))

    mapler = Mapler(next(db.session))
    mapler.run(str(os.environ.get("TOKEN")))
