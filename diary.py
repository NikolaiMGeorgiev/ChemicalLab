from models import Users, DiaryLog
from sqlalchemy import desc
from datetime import datetime
import re

class Diary():
    def __init__(self, user_id, db):
        self.user_id = user_id
        self.db = db
        self.vertical_header = "Date"
        self.header_map = {
            "chemical": "Chemical",
            "quantity": "Quantity"
        }
        self.title = "Diary logs"
        self.populate_diary_logs()

    def populate_diary_logs(self):
        with self.db.Session() as session:
            query = session.query(DiaryLog).filter(DiaryLog.user_id == self.user_id).order_by(desc(DiaryLog.date))
            grouped_logs = {}
            for log in query.all():
                date = log.date.strftime('%d.%m.%Y')
                if date not in grouped_logs:
                    grouped_logs[date] = []
                grouped_logs[date].append(log)
            self.logs = grouped_logs
    
    def __call__(self):
        col_lengths = [10, 10]
        vertical_header_length = 12
        header_texts = list(self.header_map.values())
        cols = list(self.header_map.keys())
        header = self.vertical_header + " " * (vertical_header_length - len(self.vertical_header))

        for i in range(len(col_lengths)):
            text = header_texts[i]
            offset = (col_lengths[i] - len(text)) * " "
            header += f"{text}{offset}"

        row_separator = "_" * len(header)
        print(f"{header}\n{row_separator}")

        for date, logs in self.logs.items():
            for log in logs:
                row = date + " " * (vertical_header_length - len(date)) if log == logs[0] else " " * vertical_header_length
                for i in range(len(col_lengths)):
                    text = str(log.__dict__[cols[i]])
                    offset = (col_lengths[i] - len(text)) * " "
                    row += f"{text}{offset}"
                print(row)
            print(row_separator)

    def sort_logs(self, sort_by, reverse=False):
        for logs in self.logs.values():
            logs.sort(key=lambda x: x.__dict__[sort_by], reverse=reverse)

        print("\n")
        self()
        order = "desc" if reverse else "asc"
        print(f"Sorted by: {self.header_map[sort_by].lower()} ({order})")
        print("\n")

    def get_diary_logs(self):
        return self.logs