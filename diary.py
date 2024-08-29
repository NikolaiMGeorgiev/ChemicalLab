from models import Users, DiaryLog
from sqlalchemy import desc
from datetime import datetime
import re

class Diary():
    def __init__(self, user_id, db):
        self.user_id = user_id
        self.db = db
        self.header_map = {
            "date": "Date",
            "chemical": "Chemical",
            "quantity": "Quantity"
        }
        self.title = "Diary logs"
        self.populate_diary_logs()

    def populate_diary_logs(self):
        logs = self.db.get_diary_logs(self.user_id)
        grouped_logs = {}
        for log in logs:
            log["date"] = log["date"].strftime('%d.%m.%Y')
            date = log["date"]
            if date not in grouped_logs:
                grouped_logs[date] = []
            grouped_logs[date].append(log)
        self.logs = grouped_logs
    
    def __call__(self):
        all_logs = []
        for logs in self.logs.values():
            all_logs += logs
        col_lengths = {
            "date": 12,
            "chemical": max([len(chemical) for chemical in map(lambda log: log["chemical"], all_logs)]) + 2,
            "quantity": len("quantity") + 2
        }
        cols = list(self.header_map.keys())
        header = ""

        for column in col_lengths.keys():
            header += self.header_map[column] + (col_lengths[column] - len(self.header_map[column])) * " "

        row_separator = "_" * len(header)
        print(f"{header}\n{row_separator}")

        for date, logs in self.logs.items():
            for log in logs:
                row = ""
                for column in cols:
                    if log == logs[0] and column == "date":
                        row += date + " " * (col_lengths[column] - len(date))
                    elif column == "date":
                        row += " " * col_lengths[column]
                    else:
                        row += str(log[column]) + (col_lengths[column] - len(str(log[column]))) * " "
                print(row)
            print(row_separator)

    def sort_logs(self, sort_by, reverse=False):
        if (sort_by == "date"):
            self.logs = {key: self.logs[key] for key in sorted(self.logs, reverse=reverse)}
        else:
            for logs in self.logs.values():
                logs.sort(key=lambda x: x[sort_by], reverse=reverse)
        order = "desc" if reverse else "asc"
        print(f"Sorted by: {self.header_map[sort_by].lower()} ({order})")

    def get_diary_logs(self):
        return self.logs