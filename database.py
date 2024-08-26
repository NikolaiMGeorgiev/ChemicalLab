from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Users, DiaryLog

class DB():
    def __init__(self):
        engine = create_engine("mysql://root:123456@localhost/chemical")
        self.connection = engine.connect()
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def get_user(self, user_name):
        with self.Session() as session:
            query = session.query(Users).filter(Users.name == user_name)
            return query.first()

    def add_user(self, data):
        with self.Session() as session:
            new_user = Users(
                name = data['name'],
                age = data['age'],
                weight = data['weight'],
                height = data['height'],
                bodyfat = data['bodyfat']
            )
            session.add(new_user)
            session.commit()
            return list()
    
    def add_diary_log(self, user_id, chemical, quantity, date):
        with self.Session() as session:
            new_user = DiaryLog(
                user_id = user_id,
                chemical = chemical,
                quantity = quantity,
                date = date
            )
            session.add(new_user)
            session.commit()

    def get_diary_logs(self, user_id):
        with self.Session() as session:
            query = session.query(DiaryLog).filter(DiaryLog.user_id == user_id).order_by(desc(DiaryLog.date))
            return query.all()

    def get_table_cols(self, table):
        if table == 'users':
            table_class = Users
        elif table == 'diary':
            table_class = DiaryLog
        else:
            return []
        return list(filter(lambda x: x != 'id', table_class.__table__.columns.keys()))
