from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Users, Vendors, Chats, Messages, DiaryLog, LabHistory
from config import db_user, db_password, db_name, db_server

class DB():
    def __init__(self):
        engine = create_engine(f"mysql://{db_user}:{db_password}@{db_server}/{db_name}")
        self.connection = engine.connect()
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_user(self, data):
        new_user = Users(
            name = data['name'],
            age = data['age'],
            weight = data['weight'],
            height = data['height'],
            bodyfat = data['bodyfat']
        )
        self.session.add(new_user)
        self.session.commit()
        return list()
        
    def add_chat(self, user_id, vendor_id):
        if self.get_chat_by_users(user_id, vendor_id):
            return
        new_chat = Chats(
            user_id = user_id,
            vendor_id = vendor_id
        )
        self.session.add(new_chat)
        self.session.commit()

    def add_message(self, chat_id, content, sender):
        new_message = Messages(
            chat_id = chat_id,
            content = content,
            sender = sender
        )
        self.session.add(new_message)
        self.session.commit()

    def add_diary_log(self, user_id, chemical, quantity, date):
        new_user = DiaryLog(
            user_id = user_id,
            chemical = chemical,
            quantity = quantity,
            date = date
        )
        self.session.add(new_user)
        self.session.commit()

    def add_lab_history_record(self, user_id, substance, substance_properties):
        new_record = LabHistory(
            user_id = user_id,
            substance = substance,
            muscle_mass = substance_properties["muscle_mass"],
            body_fat = substance_properties["body_fat"],
            energy = substance_properties["energy"],
            stength = substance_properties["stength"],
            cancer = substance_properties["cancer"],
            impotence = substance_properties["impotence"],
            diabetes = substance_properties["diabetes"],
            heart_disease = substance_properties["heart_disease"]
        )
        self.session.add(new_record)
        self.session.commit()

    def get_user(self, user_name):
        query = self.session.query(Users).filter(Users.name == user_name)
        return query.first()
        
    def get_vendor(self, vendor_name):
        query = self.session.query(Vendors).filter(Vendors.name == vendor_name)
        return query.first()
        
    def get_chat(self, chat_id):
        query = self.session.query(Chats).filter(Chats.id == chat_id).first()
        if query:
            return self.get_dict_result(query)
        else:
            return None
    
    def get_chat_by_users(self, user_id, vendor_id):
        query = self.session.query(Chats).filter(Chats.user_id == user_id, Chats.vendor_id == vendor_id).first()
        if query:
            return self.get_dict_result(query)
        else:
            return None
    
    def get_pending_chat(self, vendor_id):
        query = self.session.query(Chats).filter(Chats.user_id == None, Chats.vendor_id == vendor_id).order_by(desc(Chats.id)).first()
        return self.get_dict_result(query)
        
    def get_unreceived_message(self, chat_id, sender):
        message = self.session.query(Messages).filter(Messages.chat_id == chat_id, Messages.sender == sender, Messages.read == 0).first()
        if message:
            message.read = 1
            message_data = self.get_dict_result(message)
            self.session.commit()
            return message_data
        else:
            return None
        
    def get_diary_logs(self, user_id):
        query = self.session.query(DiaryLog).filter(DiaryLog.user_id == user_id).order_by(desc(DiaryLog.date))
        return [{key: value for key, value in row.__dict__.items() if key != "_sa_instance_state"} for row in query.all()]
    
    def get_lab_history(self, user_id):
        query = self.session.query(LabHistory).filter(LabHistory.user_id == user_id).order_by(LabHistory.id)
        return [{key: value for key, value in row.__dict__.items() if key != '_sa_instance_state' and key != 'id' and key != 'user_id'} for row in query.all()]

    def get_table_cols(self, table):
        if table == 'users':
            table_class = Users
        elif table == 'diary':
            table_class = DiaryLog
        else:
            return []
        return list(filter(lambda x: x != 'id', table_class.__table__.columns.keys()))
    
    def join_pending_chat(self, user_id):
        chat_data_raw = self.session.query(Chats).filter(Chats.user_id == None).order_by(Chats.id).first()
        if (chat_data_raw):
            chat_data = self.get_dict_result(chat_data_raw)
            chat_data_raw.user_id = user_id
            self.session.commit()
            return chat_data
        else:
            return None
            
    def get_dict_result(self, result):
        return {key: value for key, value in result.__dict__.items() if key != "_sa_instance_state"}