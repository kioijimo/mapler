from abc import ABC

from sqlmodel import Session, SQLModel, create_engine


class DBService(ABC):
    def __init__(self, conn_url):
        self.conn_url = conn_url
        self.conn_args = {"check_same_thread": False}
        self.init_engine()
        self.create_db()

    def init_engine(self):
        self.engine = create_engine(
            self.conn_url, connect_args=self.conn_args, echo=True
        )

    def create_db(self):
        SQLModel.metadata.create_all(self.engine)

    @property
    def session(self):
        with Session(self.engine) as session:
            yield session
